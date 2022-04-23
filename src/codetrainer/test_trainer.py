from .trainer import add_one


def test_square():
    # When
    subject = add_one(1)

    # Then
    assert subject == 2