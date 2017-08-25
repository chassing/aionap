# Sample Test passing with nose and pytest

import aionap


def test_pass():
    assert aionap.foo() == "bar"


def test_fail():
    assert False
