import re

from cli.colors import make_scheme
from main import format_team, format_title, main

_COLORS = make_scheme(no_color=False)


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def test_format_title_has_box_and_shadow() -> None:
    result = strip_ansi(format_title("Hello", _COLORS))
    assert "╔" in result
    assert "║  Hello  ║" in result
    assert "╚" in result
    assert "░" in result


def test_format_team_lists_members() -> None:
    members = [("Alice", "Lead"), ("Bob", "Developer")]
    result = strip_ansi(format_team("Team X", members, _COLORS))
    assert "Team X:" in result
    assert "● Alice" in result
    assert "(Lead)" in result
    assert "● Bob" in result
    assert "(Developer)" in result


def test_quit_command(monkeypatch, capsys) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "quit")
    main([])
    output = capsys.readouterr().out
    assert "Assistant Bot" in output
    assert "Good bye!" in output


def test_exit_command(monkeypatch, capsys) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "exit")
    main([])
    output = capsys.readouterr().out
    assert "Good bye!" in output


def test_close_command(monkeypatch, capsys) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "close")
    main([])
    output = capsys.readouterr().out
    assert "Good bye!" in output


def test_help_then_quit(monkeypatch, capsys) -> None:
    inputs = iter(["help", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main([])
    output = capsys.readouterr().out
    assert output.count("Available commands:") == 2


def test_unknown_command(monkeypatch, capsys) -> None:
    inputs = iter(["foobar", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main([])
    output = capsys.readouterr().out
    assert "Unknown command: foobar" in output


def test_unknown_command_suggests_similar(monkeypatch, capsys) -> None:
    inputs = iter(["helo", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main([])
    output = capsys.readouterr().out
    assert "Did you mean: hello?" in output


def test_eof_exits_gracefully(monkeypatch, capsys) -> None:
    def raise_eof(_: str) -> str:
        raise EOFError

    monkeypatch.setattr("builtins.input", raise_eof)
    main([])
    output = capsys.readouterr().out
    assert "Good bye!" in output


def test_unmatched_quotes(monkeypatch, capsys) -> None:
    inputs = iter(['add "hello', "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main([])
    output = capsys.readouterr().out
    assert "Invalid input: unmatched quotes." in output


def test_hello_command(monkeypatch, capsys) -> None:
    inputs = iter(["hello", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main([])
    output = capsys.readouterr().out
    assert "How can I help you?" in output


def test_greeting_includes_all_sections(monkeypatch, capsys) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "quit")
    main([])
    output = strip_ansi(capsys.readouterr().out)
    assert "Assistant Bot" in output
    assert "Team #3:" in output
    assert "● Olga Shadrunova" in output
    assert "● Oleksandr Semychenkov" in output
    assert "Available commands:" in output
