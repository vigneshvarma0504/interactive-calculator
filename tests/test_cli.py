import builtins
import importlib
import runpy
from typing import List
import pytest
from calc.cli import parse_line, run_repl, HELP_TEXT

def _iter_inputs(lines: List[str]):
    it = iter(lines)
    return lambda: next(it)

def test_parse_line_valid():
    assert parse_line("add 2 3") == ("add", 2.0, 3.0)
    assert parse_line("HELP") == ("help",)
    assert parse_line("quit") == ("quit",)

def test_parse_line_errors():
    with pytest.raises(ValueError) as e:
        parse_line("")
    assert "empty command" in str(e.value)

    with pytest.raises(ValueError) as e:
        parse_line("unknown 1 2")
    assert "unknown command" in str(e.value)

    with pytest.raises(ValueError) as e:
        parse_line("add 1")
    assert "exactly two numbers" in str(e.value)

    with pytest.raises(ValueError) as e:
        parse_line("add a b")
    assert "must be numbers" in str(e.value)

def test_repl_flow(monkeypatch, capsys):
    # Sequence: help, add, bad cmd, bad nums, div by zero, quit
    inputs = ["help", "add 2 3", "foo 1 2", "add x y", "div 1 0", "quit"]
    monkeypatch.setattr(builtins, "input", _iter_inputs(inputs))
    run_repl()
    out = capsys.readouterr().out
    assert "Interactive Calculator." in out
    assert HELP_TEXT.strip().splitlines()[0] in out
    assert "Result: 5.0" in out
    assert "Error: unknown command 'foo'" in out
    assert "Error: A and B must be numbers" in out
    assert "Error: Cannot divide by zero." in out
    assert "Goodbye!" in out

def test_repl_unexpected_error(monkeypatch, capsys):
    # Inject an operation that throws a non-ZeroDivisionError exception
    from calc import cli as cli_mod
    def boom(a, b):
        raise RuntimeError("kaboom")
    cli_mod.OPERATIONS["boom"] = boom

    inputs = ["boom 1 2", "quit"]
    monkeypatch.setattr(builtins, "input", _iter_inputs(inputs))
    cli_mod.run_repl()
    out = capsys.readouterr().out
    assert "Unexpected error: kaboom" in out
    assert "Goodbye!" in out
    del cli_mod.OPERATIONS["boom"]

def test_repl_line_is_none(capsys):
    # Covers the "if line is None" branch
    def input_none():
        return None
    run_repl(input_fn=input_none)
    out = capsys.readouterr().out
    assert "Goodbye!" in out

def test_repl_oserror(capsys):
    # Covers the (EOFError, StopIteration, OSError) except path
    def input_raises():
        raise OSError("stdin blocked by pytest")
    run_repl(input_fn=input_raises)
    out = capsys.readouterr().out
    assert "Goodbye!" in out

def test_repl_defaults_branch(monkeypatch, capsys):
    # Force default input resolution path and immediate exit
    def _raises_eof():
        raise EOFError()
    monkeypatch.setattr(builtins, "input", _raises_eof)
    run_repl()  # no args -> uses _current_input()
    out = capsys.readouterr().out
    assert "Interactive Calculator." in out
    assert "Goodbye!" in out

def test_current_input_uses_builtins_dict_branch(monkeypatch, capsys):
    # Force __builtins__ to be a dict so the dict branch is covered
    from calc import cli as cli_mod
    def fake_input():
        raise EOFError()
    monkeypatch.setattr(cli_mod, "__builtins__", {"input": fake_input})
    cli_mod.run_repl()
    out = capsys.readouterr().out
    assert "Interactive Calculator." in out
    assert "Goodbye!" in out

def test_main_runs_as_script(monkeypatch, capsys):
    # Run "python main.py" via runpy to hit the __main__ guard
    def fake_input():
        raise EOFError()
    monkeypatch.setattr(builtins, "input", fake_input)
    runpy.run_path("main.py", run_name="__main__")
    out = capsys.readouterr().out
    assert "Interactive Calculator." in out
    assert "Goodbye!" in out

def test_import_main_module_only():
    # Keep this lightweight import test to satisfy any module-level coverage
    m = importlib.import_module("main")
    assert hasattr(m, "__name__")
def test_current_input_module_branch(monkeypatch):
    # Force __builtins__ in calc.cli to behave like a module with an 'input' attribute
    from types import SimpleNamespace
    from calc import cli as cli_mod

    def fake_input():
        # We don't need to call it; just ensure _current_input returns it
        raise EOFError()

    # Make __builtins__ look like a module object
    monkeypatch.setattr(cli_mod, "__builtins__", SimpleNamespace(input=fake_input))

    # Call the helper directly to hit the 'return b.input' line
    fn = cli_mod._current_input()
    assert callable(fn)
