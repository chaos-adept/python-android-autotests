from .trainer import generate, compile_sample, run
from ..logging_utils import config

config.setup_logging()

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


def test_compilation(tmp_path):
    # Given
    code_fragment = "int name = 1;"
    code, java_class = compile_sample(code_fragment, tmp_path)
    assert code == 0

    # When
    code, stdout, stderr = run(java_class, tmp_path)

    # Then
    assert code == 0, f'unexpected error code:{code}, stderr:{stderr}'
    assert stdout == b"Hello World! 1\r\n"
