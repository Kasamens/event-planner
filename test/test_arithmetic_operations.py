

def add(a: int, b: int) -> int:
    return a + b

def subtract(a: int, b: int) -> int:
    return a - b

def multiply(a: int, b: int) -> int:
    return a * b

def divide(a: int, b: int) -> int:
    return a // b

def test_add() -> None:
    assert add(1, 1) == 2

def test_subtract() -> None:
    assert subtract(5, 2) == 3

def test_multiply() -> None:
    assert multiply(2,4) == 8

def test_divide() -> None:
    assert divide(8,4) == 2