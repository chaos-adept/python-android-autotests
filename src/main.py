import logging
import sys
import tempfile

from codetrainer import trainer
from logging_utils import config

if __name__ == "__main__":
    config.setup_logging()

    logging.info("code trainer started")

    logging.info("start input reading")
    code_fragment = sys.stdin.read()
    logging.info("code fragment \n%s", code_fragment)

    with tempfile.TemporaryDirectory() as working_dir:

        trainer.verify_preconditions(code_fragment)

        # todo format compilation errors correctly
        java_class = trainer.compile_fragment(code_fragment=code_fragment, working_dir=working_dir,
                                              template_name='compilation_checker', class_name='CompilationChecker')

        # generation fragment for test cases
        test_case_java_class = trainer.compile_testcase_runner(code_fragment, working_dir)

        # format timeout errors correctly
        trainer.assert_io(test_case_java_class, working_dir, "0", "")
        trainer.assert_io(test_case_java_class, working_dir, "3", ('\n'.join(str(x*x) for x in range(0, 3)) + '\n') * 2)

        stdout = trainer.run(java_class, working_dir)
        logging.info("Original samples run results: '%s'", stdout)
        sys.stdout.write(stdout)

        logging.info("code trainer finished")
