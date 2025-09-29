from typing import Callable, Tuple
from . import operations as ops

OPERATIONS = {
    "add": ops.add,
    "sub": ops.sub,
    "mul": ops.mul,
    "div": ops.div,
}

HELP_TEXT = """Commands:
  add A B   -> A + B
  sub A B   -> A - B
  mul A B   -> A * B
  div A B   -> A / B
  help      -> show this help
  quit      -> exit
Examples:
  add 2 3
  div 10 4
"""

def parse_line(line: str) -> Tuple[str, float, float] | Tuple[str]:
    """
    Returns:
      ("quit",) or ("help",) OR (op, a, b)
    Raises:
      ValueError when the command is malformed
    """
    tokens = line.strip().split()
    if not tokens:
        raise ValueError("empty command")

    cmd = tokens[0].lower()
    if cmd == "quit":
        return ("quit",)
    if cmd == "help":
        return ("help",)

    if cmd not in OPERATIONS:
        raise ValueError(f"unknown command '{cmd}'")

    if len(tokens) != 3:
        raise ValueError("expected exactly two numbers, e.g. 'add 2 3'")

    try:
        a = float(tokens[1])
        b = float(tokens[2])
    except ValueError:
        raise ValueError("A and B must be numbers")

    return (cmd, a, b)

def _current_input() -> Callable[[], str]:
    """
    Resolve the current builtins.input at call time so test monkeypatching works.
    Covers both cases where __builtins__ is a dict or a module.
    """
    b = __builtins__
    if isinstance(b, dict):
        return b["input"]  # pragma: no cover
    # else: module
    return b.input  # type: ignore[attr-defined]


def run_repl(
    input_fn: Callable[[], str] | None = None,
    output_fn: Callable[..., None] | None = None,
) -> None:
    # Resolve defaults at runtime (important for pytest monkeypatch)
    if input_fn is None:
        input_fn = _current_input()
    if output_fn is None:
        output_fn = print

    output_fn("Interactive Calculator. Type 'help' for commands, 'quit' to exit.")
    while True:
        output_fn("> ", end="")
        try:
            line = input_fn()
        except (EOFError, StopIteration, OSError):
            # Treat any read/capture error under pytest as EOF
            output_fn("\nGoodbye!")
            break

        if line is None:
            output_fn("Goodbye!")
            break

        try:
            parsed = parse_line(line)
            if parsed[0] == "quit":
                output_fn("Goodbye!")
                break
            if parsed[0] == "help":
                output_fn(HELP_TEXT)
                continue

            op, a, b = parsed  # type: ignore
            try:
                result = OPERATIONS[op](a, b)  # type: ignore[index]
                output_fn(f"Result: {result}")
            except ZeroDivisionError:
                output_fn("Error: Cannot divide by zero.")
        except ValueError as e:
            output_fn(f"Error: {e}")
        except Exception as e:
            # Safety net: keep REPL running and show message
            output_fn(f"Unexpected error: {e}")
