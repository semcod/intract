def add(a: float, b: float) -> float:
    # This is a pure function
    return a + b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def write_to_log(msg: str) -> None:
    # A side-effectful write function
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(msg + "\n")
