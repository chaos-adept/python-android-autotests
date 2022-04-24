import os
import subprocess

from string import Template

class_name = "HelloWorldApp"
classTemplate = Template("""
    class ${class_name} {
        public static void main(String[] args) {
            ${code_fragment}
            System.out.println("Hello World! " + name);
        }
    }
""")


def generate(code_fragment):
    return classTemplate.substitute(class_name=class_name, code_fragment=code_fragment)


def compile_sample(code_fragment, working_dir):
    java_file = os.path.join(working_dir.name, f"{class_name}.java")
    java_class = class_name
    with open(java_file, "w") as f:
        f.write(generate(code_fragment=code_fragment))
    cmd = [f"javac", java_file]
    r = subprocess.run(cmd, capture_output=True, timeout=15, check=True)

    return r.returncode, java_class


def run(class_name, dir):
    # todo try to use py4j https://www.py4j.org/getting_started.html#writing-the-java-program
    cmd = ['java', f'-cp', dir.name, class_name]
    r = subprocess.run(cmd, capture_output=True, timeout=15, check=True)
    return r.returncode, r.stdout, r.stderr
