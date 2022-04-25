import logging
import os
import sys

from logging_utils import config

from codetrainer import trainer

if __name__ == "__main__":
    config.setup_logging()
    logging.info("code trainer started")

    code_fragment = sys.stdin.read()
    logging.info("code fragment \n%s", code_fragment)

    working_dir = os.getcwd()
    java_class = trainer.compile_sample(code_fragment=code_fragment, working_dir=working_dir)
    code, stdout, stderr = trainer.run(java_class, working_dir)
    logging.debug("run results", stdout)

    logging.info("code trainer finished")
