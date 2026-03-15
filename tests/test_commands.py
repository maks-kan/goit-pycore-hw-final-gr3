import pytest

from cli.colors import make_scheme
from cli.commands import (
    command,
    handle_echo,
    handle_greet,
    handle_help,
    handle_quit,
)
from main import AddressBook, bootstrap_commands

_COLORS = make_scheme(no_color=False)


def test_command_decorator_sets_docstring() -> None:
    @command("Test help text.")
    def dummy() -> int:
        return 42

    assert dummy.__doc__ == "Test help text."
    assert dummy() == 42


def test_handle_echo_returns_numbered_args() -> None:
    assert handle_echo("hello", "world") == "  1: hello\n  2: world"


def test_handle_echo_no_args() -> None:
    assert handle_echo() == "(no arguments)"


def test_handle_greet_with_name() -> None:
    result = handle_greet("Alice", colors=_COLORS)
    assert "Hello, Alice!" in result


def test_handle_greet_without_name_raises() -> None:
    with pytest.raises(ValueError, match="name is required"):
        handle_greet(colors=_COLORS)


def test_handle_quit_returns_farewell() -> None:
    assert "Good bye!" in handle_quit(colors=_COLORS)


def test_handle_help_lists_all_commands() -> None:
    commands = bootstrap_commands(_COLORS, AddressBook())
    result = handle_help(commands, colors=_COLORS)
    assert "Available commands:" in result
    assert "help" in result
    assert "quit" in result
    assert "Show available commands." in result
    assert "Exit the assistant bot." in result
