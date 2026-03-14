from cli.commands import (
    command,
    default_commands,
    handle_echo,
    handle_help,
    handle_quit,
)


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


def test_handle_quit_returns_farewell() -> None:
    assert handle_quit() == "Good bye!"


def test_handle_help_lists_all_commands() -> None:
    commands = default_commands()
    result = handle_help(commands)
    assert "Available commands:" in result
    assert "help" in result
    assert "quit" in result
    assert "Show available commands." in result
    assert "Exit the assistant bot." in result
