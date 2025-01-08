# pylint: disable=comparison-of-constants,comparison-with-itself
def test_that_cannot_fail():
    assert 1 == 1
    assert "abc" != "def"
