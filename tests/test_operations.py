import pytest
from calc import operations as ops

@pytest.mark.parametrize(
    "a,b,expected",
    [(0, 0, 0.0), (2, 3, 5.0), (-2, 3, 1.0), (2.5, 0.5, 3.0)],
)
def test_add(a, b, expected):
    assert ops.add(a, b) == pytest.approx(expected)

@pytest.mark.parametrize(
    "a,b,expected",
    [(0, 0, 0.0), (5, 3, 2.0), (-2, -3, 1.0), (2.5, 0.5, 2.0)],
)
def test_sub(a, b, expected):
    assert ops.sub(a, b) == pytest.approx(expected)

@pytest.mark.parametrize(
    "a,b,expected",
    [(0, 0, 0.0), (2, 3, 6.0), (-2, 3, -6.0), (2.5, 0.5, 1.25)],
)
def test_mul(a, b, expected):
    assert ops.mul(a, b) == pytest.approx(expected)

@pytest.mark.parametrize(
    "a,b,expected",
    [(0, 1, 0.0), (6, 3, 2.0), (-6, 3, -2.0), (2.5, 0.5, 5.0)],
)
def test_div(a, b, expected):
    assert ops.div(a, b) == pytest.approx(expected)

def test_div_by_zero():
    with pytest.raises(ZeroDivisionError):
        ops.div(1, 0)
