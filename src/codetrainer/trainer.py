import logging
import os
import re
import subprocess
from .errors import CompilationError, VerificationFailedError
from pathlib import Path
from string import Template

# logger = logging.getLogger(__name__)

# todo extract env variables with default value
default_timeout = 15


def generate(code_fragment, template_name, class_name):
    template_path = Path(__file__).resolve().parent / f"data/templates/{template_name}.template"
    template_str_lines = open(template_path, "r").readlines()

    # todo rewrite in the python way
    offset = 0
    for idx, line in enumerate(template_str_lines):
        if "${code_fragment}" in line:
            offset = idx
            break

    class_template = Template(''.join(template_str_lines))
    generated = class_template.substitute(class_name=class_name, code_fragment=code_fragment)
    logging.info("generated finished offset=%s generated source=%s", offset, generated)

    return generated, offset


def to_compilation_error(stderr, offset=0):
    regexp = rf'.+\.java:(\d+):'

    def translate_offset(matchobj):
        val = int(matchobj.group(1))
        return f"line:{str(val - offset)}:"

    translated = re.sub(regexp, translate_offset, stderr)

    regexp_class_location = r'\s+location\: class .+\s*\n'
    translated = re.sub(regexp_class_location, '\n\n', translated)
    return CompilationError(translated)


def compile_fragment(code_fragment, working_dir, template_name, class_name):
    logging.info("compile sample %s template %s", code_fragment, template_name)
    java_file = os.path.join(working_dir, f"{class_name}.java")
    java_class = class_name
    generated_source, offset = generate(code_fragment, template_name, class_name=class_name)
    logging.info("generated source offset=%s, '%s'", offset, generated_source)
    with open(java_file, "w") as f:
        f.write(generated_source)

    cmd = [f"javac", java_file]
    try:
        subprocess.run(cmd, capture_output=True, timeout=default_timeout, check=True, text=True, encoding="utf-8")
    except subprocess.CalledProcessError as err:
        logging.critical(err, exc_info=True)
        logging.error("compilation process failed with stderr %s", err.stderr)

        # transform compilation issues
        raise to_compilation_error(err.stderr, offset=offset)

    return java_class


def run(class_name, working_dir, stdin=None):
    cmd = ['java', f'-cp', working_dir, class_name]
    logging.info("run java with args %s , input=%s", cmd, stdin)
    try:
        r = subprocess.run(cmd, input=stdin, text=True, capture_output=True, timeout=default_timeout, check=True,
                           encoding="utf-8")
        return r.stdout
    except subprocess.CalledProcessError as e:
        logging.error("run failed with returncode:%s stdout:%s, stderr:%s", e.returncode, e.stdout, e.stderr)
        raise e


def verify_declarations(type_name, name, value, code_fragment):
    logging.info("verify variable declaration type=%s, name=%s, value=%s", type_name, name, value)
    expected = 1
    regexp = rf"{type_name}\s+{name}\s*=\s*{value}"
    logging.debug("regexp %s", regexp)
    actual = len(re.findall(regexp, code_fragment))

    if actual != expected:
        raise VerificationFailedError(
            f"Unexpected number of variable declaration '{name}' declaration, expected {expected} but {actual}")


def verify_statement(statement, regexp, code_fragment, min_num, max_num=-1):
    logging.info("verify statement='%s' by regexp='%s' min_num=%s, max_num=%s", statement, regexp, min_num, max_num)
    actual = len(re.findall(regexp, code_fragment))

    if not (actual >= min_num):
        raise VerificationFailedError(
            f"'{statement}' statement needs to be presented at least {min_num} times")

    if not (max_num < 0 or actual <= max_num):
        raise VerificationFailedError(
            f"'{statement}' statement needs to be presented less than {max_num} times")


def verify_preconditions(code_fragment):
    logging.info("started precondition verification")
    # todo look into a ast realization
    # it has no variable renaming

    verify_declarations("int", "n", r"\d+", code_fragment)
    verify_declarations(r"int\[\]", "arr", r"new int\[n\]", code_fragment)

    verify_statement("for", regexp=r"\s*for\s*\(", code_fragment=code_fragment, min_num=1)
    verify_statement("while", regexp=r"\s*while\s*\(", code_fragment=code_fragment, min_num=0, max_num=0)
    verify_statement("'arr' printing", regexp=r"System.out.println\(.*arr\[", code_fragment=code_fragment, min_num=1)


def generate_test_case_fragment(original_code_fragment):
    return re.sub(r"int\s+n\s*=\s*\d+\s*;", "", original_code_fragment)


def compile_testcase_runner(original_code_fragment, working_dir):
    testcase_code_fragment = generate_test_case_fragment(original_code_fragment)
    logging.info("compiled test case code fragment %s", testcase_code_fragment)
    return compile_fragment(testcase_code_fragment, working_dir, 'testcases_runner', class_name="TestCaseRunner")


def assert_java_run_io(class_name, working_dir, stdin, expected_stdout):
    actual = run(class_name=class_name, working_dir=working_dir, stdin=stdin)
    if not (actual == expected_stdout):
        raise VerificationFailedError(
            f"Actual output different expected. actual='\n{actual}\n' but expected='\n{expected_stdout}\n'")
