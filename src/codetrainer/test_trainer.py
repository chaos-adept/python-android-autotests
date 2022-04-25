from .trainer import generate, compile_sample, run
from ..logging_utils import config

config.setup_logging()


def test_generation():
    # Given
    expected = """class CompilationChecker {
    public static void main(String[] args) {
        String name = "Bob";
    }
}
"""

    # When
    code = generate("String name = \"Bob\";")

    # Then
    assert expected == code


def test_compilation(tmp_path):
    # Given
    code_fragment = "System.out.print(\"Hello World!\");"
    java_class = compile_sample(code_fragment, tmp_path)

    # When
    stdout = run(java_class, tmp_path)

    # Then
    assert stdout == b"Hello World!"
