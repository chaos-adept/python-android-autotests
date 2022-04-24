from sys import stderr
from .trainer import generate, compile_sample, run
import tempfile

def test_generation():
    # Given
    expected = """
    class HelloWorldApp {
        public static void main(String[] args) {
            String name = "Bob";
            System.out.println("Hello World! " + name);
        }
    }
"""

    # When
    code = generate("String name = \"Bob\";")

    # Then
    assert expected == code


def test_compilation():
    # Given
    code_fragment = "int name = 1;"
    working_dir = tempfile.TemporaryDirectory()
    code, java_class = compile_sample(code_fragment, working_dir)
    assert code == 0

    # When
    code, stdout, stderr = run(java_class, working_dir)
    working_dir.cleanup()
    # Then
    assert code == 0, f'unexpected error code:{code}, stderr:{stderr}'
    assert stdout == b"Hello World! 1\r\n"
