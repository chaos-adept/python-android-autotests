import pytest

from ..codetrainer import trainer
from ..codetrainer import errors

from ..logging_utils import config

config.setup_logging()


def test_generation():
    # Given
    expected = """class TestGeneration {
    public static void main(String[] args) {
        String name = "Bob";
    }
}
"""

    # When
    code, offset = trainer.generate("String name = \"Bob\";", template_name='compilation_checker',
                                    class_name='TestGeneration')

    # Then
    assert expected == code
    assert offset == 2


def test_compilation(tmp_path):
    # Given
    code_fragment = "System.out.print(\"Hello World!\");"
    java_class = trainer.compile_fragment(code_fragment, tmp_path, template_name='compilation_checker',
                                          class_name='Any')

    # When
    stdout = trainer.run(java_class, tmp_path)

    # Then
    assert stdout == "Hello World!"


def test_transform_compilation_messages(tmp_path):
    # Given
    code_fragment = "System.out.print(\"Hello World!\"); with compilation issue;"

    # When
    with pytest.raises(errors.CompilationError) as exc_info:
        trainer.compile_fragment(code_fragment, tmp_path, template_name='compilation_checker',
                                 class_name='Any')

    assert exc_info.value.message == '''line:1: error: ';' expected
        System.out.print("Hello World!"); with compilation issue;
                                                          ^
line:1: error: not a statement
        System.out.print("Hello World!"); with compilation issue;
                                                           ^
2 errors
'''


# todo verify failing when assets are missing
def test_precondition():
    # Given
    code_fragment = """
    int n =  2;
    int[] arr = new int[n];
    for (
    System.out.println(arr[0]);
    """

    # When
    trainer.verify_preconditions(code_fragment)

    # Then
    pass


def test_compile_testcase_runner():
    # Given
    code_fragment = """
    int n =  2;
    int[] arr = new int[n];
    for (
    """
    expected = """
    
    int[] arr = new int[n];
    for (
    """

    # When
    actual = trainer.generate_test_case_fragment(code_fragment)

    # Then
    assert actual == expected


def test_assertio(tmp_path):
    # Given
    code_fragment = "System.out.println(1);"
    java_class = trainer.compile_fragment(code_fragment, tmp_path, template_name='compilation_checker',
                                          class_name='Any')

    # When
    trainer.assert_java_run_io(java_class, tmp_path, "any", "1\n")

    # Then
    pass
