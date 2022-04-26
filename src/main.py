import logging
import sys
import tempfile

from codetrainer.errors import PreconditionFailedError, CompilationError
from codetrainer import trainer
from logging_utils import config


def run_autotest(code_fragment, stdout = sys.stdout):
    logging.info("code trainer started")
    logging.info("code fragment \n%s", code_fragment)

    with tempfile.TemporaryDirectory() as working_dir:
        try:
            trainer.verify_preconditions(code_fragment)
        except PreconditionFailedError as e:
            logging.critical(e)
            stdout.write(f"Precondition failed. Reason: {e.message}")
            return

        try:
            java_class = trainer.compile_fragment(code_fragment=code_fragment, working_dir=working_dir,
                                                  template_name='compilation_checker', class_name='CompilationChecker')
        except CompilationError as e:
            logging.critical(e)
            stdout.write(f"Compilation failed. Reason: {e.message}")
            return

        # generation fragment for test cases
        test_case_java_class = trainer.compile_testcase_runner(code_fragment, working_dir)

        # format timeout errors correctly
        try:
            trainer.assert_java_run_io(test_case_java_class, working_dir, "0", "")
            trainer.assert_java_run_io(test_case_java_class, working_dir, "3",
                                       ('\n'.join(str(x * x) for x in range(0, 3)) + '\n') * 2)
        except AssertionError as e:
            logging.critical(e)
            stdout.write(f"Verification Steps Failed. Reason: {e}")
            return

        result = trainer.run(java_class, working_dir)
        logging.info("Original samples run results: '%s'", result)
        stdout.write(result)
        logging.info("code trainer finished")
        return True


if __name__ == "__main__":
    config.setup_logging()
    if not run_autotest(sys.stdin.read()):
        sys.exit(1)
