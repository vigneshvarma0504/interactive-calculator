from typing import Union

Number = Union[int, float]

def _to_float(x: Number) -> float:
    return float(x)

def add(a: Number, b: Number) -> float:
    return _to_float(a) + _to_float(b)

def sub(a: Number, b: Number) -> float:
    return _to_float(a) - _to_float(b)

def mul(a: Number, b: Number) -> float:
    return _to_float(a) * _to_float(b)

def div(a: Number, b: Number) -> float:
    b = _to_float(b)
    if b == 0.0:
        raise ZeroDivisionError("division by zero")
    return _to_float(a) / b
