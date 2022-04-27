import logging
import sys
import tempfile

from codetrainer.errors import VerificationFailedError, CompilationError, JavaRunFailedError
from codetrainer import trainer
from logging_utils import config


def run_autotest(code_fragment, stdout=sys.stdout):
    logging.info("code trainer started")
    logging.info("code fragment \n%s", code_fragment)

    with tempfile.TemporaryDirectory() as working_dir:
        try:
            trainer.verify_preconditions(code_fragment)
        except VerificationFailedError as e:
            logging.critical(e)
            stdout.write(f"Precondition failed. Reason: {e.message}")
            return

        try:
            java_class, code_fragment_offset = trainer.compile_fragment(code_fragment=code_fragment,
                                                                        working_dir=working_dir,
                                                                        template_name='compilation_checker',
                                                                        class_name='CompilationChecker')
        except CompilationError as e:
            logging.critical(e)
            stdout.write(f"Compilation failed. Reason: {e.message}")
            return

        try:
            result = trainer.run(java_class, working_dir, stdin=None, code_fragment_offset=code_fragment_offset)
            logging.info("Original samples run results: '%s'", result)
        except JavaRunFailedError as e:
            stdout.write(f"Run failed. Reason: {e.message}")
            return

        # generation fragment for test cases
        test_case_java_class, test_fragment_offset = trainer.compile_testcase_runner(code_fragment, working_dir)

        # format timeout errors correctly
        try:
            trainer.assert_java_run_io(test_case_java_class, working_dir, "0", "")
            trainer.assert_java_run_io(test_case_java_class, working_dir, "3",
                                       ('\n'.join(str(x * x) for x in range(0, 3)) + '\n') * 2)
        except JavaRunFailedError as e:
            stdout.write(f"Test-Case Steps Verification Runtime Failed. Reason: {e}")
            return
        except VerificationFailedError as e:
            logging.critical(e)
            stdout.write(f"Test-Case Steps Verification Check Failed. Reason: {e}")
            return

        stdout.write(result)
        logging.info("code trainer finished")
        return True


if __name__ == "__main__":
    config.setup_logging()
    if not run_autotest(sys.stdin.read()):
        sys.exit(1)
