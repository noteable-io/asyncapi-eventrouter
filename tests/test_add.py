import pytest

from asyncapi_eventrouter import add


def test_working_add():
    x = 2
    y = 2
    assert add(x, y) == 4


def test_not_working_add():
    x = 2
    y = 2
    with pytest.raises(AssertionError):
        assert add(x, y) == 5
