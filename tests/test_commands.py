from cli.colors import make_scheme
from cli.commands import (
    command,
    handle_help,
    handle_quit,
)
from main import bootstrap_commands
from models.address_book import AddressBook
from models.notebook import NoteBook

_COLORS = make_scheme(no_color=False)


def test_command_decorator_sets_docstring() -> None:
    @command("Test help text.")
    def dummy() -> int:
        return 42

    assert dummy.__doc__ == "Test help text."
    assert dummy() == 42


def test_handle_quit_returns_farewell() -> None:
    assert "Good bye!" in handle_quit(colors=_COLORS)


def test_handle_help_lists_all_commands() -> None:
    commands = bootstrap_commands(_COLORS, AddressBook(), NoteBook())
    result = handle_help(commands, colors=_COLORS)
    assert "Available commands:" in result
    assert "help" in result
    assert "quit" in result
    assert "hello" in result
    assert "add" in result
    assert "add-note" in result
