import subprocess
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
    r = subprocess.run(["python", "src/main.py"], input=sample(from_name), text=True,
                       shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       timeout=default_timeout, check=True,
                       encoding="utf-8")
    assert r.stdout == expected(from_name)


def test_basic_flow_for_author_solution():
    e2e_run('author_solution')