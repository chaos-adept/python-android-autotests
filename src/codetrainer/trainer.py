import logging
import os
import subprocess
from string import Template
from pathlib import Path

logger = logging.getLogger(__name__)

class_name = "CompilationChecker"


def generate(code_fragment):
    template_path = Path(__file__).resolve().parent / "data/templates/compilation_checker.template"
    template_str = open(template_path, "r").read()
    class_template = Template(template_str)
    return class_template.substitute(class_name=class_name, code_fragment=code_fragment)


def compile_sample(code_fragment, working_dir):
    logger.info("compile sample %s", code_fragment)
    java_file = os.path.join(working_dir, f"{class_name}.java")
    java_class = class_name
    generated_source = generate(code_fragment=code_fragment)
    logger.debug("generated source %s", generated_source)
    with open(java_file, "w") as f:
        f.write(generated_source)
    cmd = [f"javac", java_file]
    subprocess.run(cmd, capture_output=True, timeout=15, check=True)

    return java_class


def run(class_name, dir):
    # todo try to use py4j https://www.py4j.org/getting_started.html#writing-the-java-program
    cmd = ['java', f'-cp', dir, class_name]
    logger.info("run java with args %s", cmd)
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=15, check=True)
    except subprocess.CalledProcessError as e:
        logger.error("run failed with returncode:%s stdout:%s, stderr:%s", e.returncode, e.stdout, e.stderr)
    return r.stdout
