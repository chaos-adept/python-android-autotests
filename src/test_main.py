import subprocess
import logging
from pathlib import Path

from .logging_utils import config

config.setup_logging()

samples_path = Path(__file__).resolve().parent / f"samples"

default_timeout = 5


def sample(from_name):
    return (samples_path / f"{from_name}.java_fragment").read_text()


def expected(from_name):
    return (samples_path / f"{from_name}.expected_output").read_text()


def e2e_run(from_name):
    stdin = sample(from_name)
    r = subprocess.run(["python", "src/main.py"], input=stdin, text=True,
                       shell=False,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       timeout=default_timeout, check=False,
                       encoding="utf-8")
    expected_result = expected(from_name)

    logging.debug("stdin '%s'", stdin)
    logging.debug("actual results stdin='%s'", r.stdout)
    logging.debug("expected results '%s'", expected_result)
    assert r.stdout == expected_result


def test_basic_flow_for_author_solution():
    e2e_run('author_solution')

def test_exception_flow_compilation_issue():
    e2e_run('sample_compilation_issue')

def test_exception_runtime_issue():
    e2e_run('sample_runtime_issue')
