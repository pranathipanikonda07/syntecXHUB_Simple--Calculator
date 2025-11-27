"""Simple CLI calculator

Supports +, -, *, / and a clear command. Calculation logic is separated into
functions for testability.
"""
from typing import Tuple, Optional


class CalculationError(Exception):
    pass


def calculate(a: float, op: str, b: float) -> float:
    """Perform basic arithmetic between two numbers.

    Raises CalculationError for unknown operators or divide-by-zero.
    """
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise CalculationError("Division by zero")
        return a / b
    raise CalculationError(f"Unsupported operator: {op}")


def parse_input(line: str) -> Tuple[str, Optional[float], Optional[str], Optional[float]]:
    """Parse a user input line and return a tuple describing the action.

    Returns one of:
      - ("operator", a, op, b) where operator is "+", "-", "*", or "/"
      - ("clear", None, None, None) if the user typed 'clear'
      - ("exit", None, None, None) if the user typed 'exit' or 'quit'

    Raises CalculationError for bad formatting or invalid numbers.
    """
    text = line.strip()
    if text == "":
        raise CalculationError("Empty input")

    lowered = text.lower()
    if lowered in ("exit", "quit"):
        return ("exit", None, None, None)
    if lowered == "clear":
        return ("clear", None, None, None)

    # Expect format: <number> <op> <number>, where op is one of + - * /
    parts = text.split()
    if len(parts) != 3:
        raise CalculationError("Input must be: <number> <operator> <number>")

    a_str, op, b_str = parts
    if op not in ("+", "-", "*", "/"):
        raise CalculationError(f"Unsupported operator: {op}")

    try:
        a = float(a_str)
    except ValueError:
        raise CalculationError(f"Invalid number: {a_str}")

    try:
        b = float(b_str)
    except ValueError:
        raise CalculationError(f"Invalid number: {b_str}")

    return (op, a, op, b)


def run_cli() -> None:
    """Run a simple command-line loop for calculations.

    Commands supported:
      <number> <operator> <number> -- evaluate an expression
      clear                        -- resets stored result/context
      exit|quit                    -- quit the program

    This function is intentionally thin — calculation logic is in calculate()
    so it remains easy to unit test.
    """
    print("Simple Calculator — enter expressions like: 3 + 4")
    print("Commands: clear, exit, quit")

    last_result: Optional[float] = None

    while True:
        try:
            raw = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nGoodbye')
            break

        if not raw:
            continue

        try:
            action = parse_input(raw)
        except CalculationError as e:
            print(f"Error: {e}")
            continue

        if action[0] == "exit":
            print("Exiting — goodbye")
            break
        if action[0] == "clear":
            last_result = None
            print("Cleared")
            continue

        # action expected to be (op, a, op, b)
        _, a, op, b = action
        try:
            result = calculate(a, op, b)
        except CalculationError as e:
            print(f"Error: {e}")
            continue

        last_result = result
        # print integer-looking numbers as ints
        if float(result).is_integer():
            print(int(result))
        else:
            print(result)


if __name__ == "__main__":
    run_cli()
