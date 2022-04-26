import logging
import os
import re
import subprocess
from pathlib import Path
from string import Template

logger = logging.getLogger(__name__)

default_timeout = 15


def generate(code_fragment, template_name, class_name):
    template_path = Path(__file__).resolve().parent / f"data/templates/{template_name}.template"
    template_str = open(template_path, "r").read()
    class_template = Template(template_str)
    return class_template.substitute(class_name=class_name, code_fragment=code_fragment)


def compile_fragment(code_fragment, working_dir, template_name, class_name):
    logger.info("compile sample %s template %s", code_fragment, template_name)
    java_file = os.path.join(working_dir, f"{class_name}.java")
    java_class = class_name
    generated_source = generate(code_fragment, template_name, class_name=class_name)
    logger.info("generated source %s", generated_source)
    with open(java_file, "w") as f:
        f.write(generated_source)

    cmd = [f"javac", java_file]
    try:
        subprocess.run(cmd, capture_output=True, timeout=default_timeout, check=True, text=True, encoding="utf-8")
    except subprocess.CalledProcessError as err:
        logger.critical(err, exc_info=True)
        logger.error("compilation process failed with stderr %s", err.stderr)
        raise err

    return java_class


def run(class_name, working_dir, stdin=None):
    cmd = ['java', f'-cp', working_dir, class_name]
    logger.info("run java with args %s , input=%s", cmd, stdin)
    try:
        r = subprocess.run(cmd, input=stdin, text=True, capture_output=True, timeout=default_timeout, check=True,
                           encoding="utf-8")
        return r.stdout
    except subprocess.CalledProcessError as e:
        logger.error("run failed with returncode:%s stdout:%s, stderr:%s", e.returncode, e.stdout, e.stderr)
        raise e


def verify_var_initialization(type_name, name, value, code_fragment):
    logger.info("verify variable declaration type=%s, name=%s, value=%s", type_name, name, value)
    expected = 1
    actual = len(re.findall(rf"{type_name}\s+{name}\s*=\s*{value}", code_fragment))

    assert actual == expected, \
        f"Unexpected number of variable declaration '{name}' declaration, expected {expected} but {actual}"


def verify_statement(statement, regexp, code_fragment, min_num, max_num=-1):
    logger.info("verify statement='%s' by regexp='%s' min_num=%s, max_num=%s", statement, regexp, min_num, max_num)
    actual = len(re.findall(regexp, code_fragment))

    assert actual >= min_num, \
        f"'{statement}' statement needs to be presented at least {min_num} times"

    assert max_num < 0 or actual <= max_num, \
        f"'{statement}' statement needs to be presented less than {max_num} times"


def verify_preconditions(code_fragment):
    logger.info("started precondition verification")
    # todo look into a ast realization
    # it has no variable renaming

    verify_var_initialization("int", "n", r"\d+", code_fragment)
    verify_var_initialization(r"int\[\]", "arr", r"new int\[n\]", code_fragment)

    verify_statement("for", regexp=r"\s*for\s*\(", code_fragment=code_fragment, min_num=1)
    verify_statement("while", regexp=r"\s*while\s*\(", code_fragment=code_fragment, min_num=0, max_num=0)
    verify_statement("'arr' printing", regexp=r"System.out.println\(.*arr\[", code_fragment=code_fragment, min_num=1)


def generate_test_case_fragment(original_code_fragment):
    return re.sub(r"int\s+n\s*=\s*\d+\s*;", "", original_code_fragment)


def compile_testcase_runner(original_code_fragment, working_dir):
    testcase_code_fragment = generate_test_case_fragment(original_code_fragment)
    logger.info("compiled test case code fragment %s", testcase_code_fragment)
    return compile_fragment(testcase_code_fragment, working_dir, 'testcases_runner', class_name="TestCaseRunner")


def assert_io(class_name, working_dir, stdin, expected_stdout):
    actual = run(class_name=class_name, working_dir=working_dir, stdin=stdin)
    assert actual == expected_stdout, \
        f"Actual output different expected. actual='\n{actual}\n' but expected='\n{expected_stdout}\n'"
