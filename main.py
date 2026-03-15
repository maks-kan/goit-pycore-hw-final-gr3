import argparse
import os
from collections.abc import Callable
from functools import partial
from typing import Any

from cli.colors import ColorScheme, make_scheme
from cli.commands import handle_help, handle_quit
from cli.repl import run_repl
from handlers.contact_handlers import (
    handle_add_birthday,
    handle_add_contact,
    handle_add_email,
    handle_birthdays,
    handle_change_birthday,
    handle_change_email,
    handle_change_phone,
    handle_delete_contact,
    handle_hello,
    handle_remove_birthday,
    handle_remove_email,
    handle_remove_phone,
    handle_search,
    handle_show_all,
    handle_show_birthday,
    handle_show_email,
    handle_show_phone,
)
from handlers.note_handlers import (
    handle_add_note,
    handle_delete_note,
    handle_edit_note,
    handle_search_notes,
    handle_show_all_notes,
)
from models.address_book import AddressBook
from models.notebook import NoteBook
from storage import load_contacts, load_notes, save_contacts, save_notes

TITLE = "Assistant Bot"
TEAM_NAME = "Team #3"
TEAM_MEMBERS = [
    ("Maks Kaniuka", "Team Lead"),
    ("Olga Shadrunova", "Developer 1"),
    ("Ivan Bochkarov", "Developer 2"),
    ("Oleksandr Semychenkov", "Developer 3"),
]


def format_title(title: str, colors: ColorScheme) -> str:
    """Format title in a Unicode box with shadow."""
    width = len(title) + 4
    box = "═" * width
    shadow_line = "░" * (width + 2)
    return (
        f"  {colors.TITLE}╔{box}╗{colors.RESET}\n"
        f"  {colors.TITLE}║  {title}  ║{colors.RESET}{colors.SHADOW}░{colors.RESET}\n"
        f"  {colors.TITLE}╚{box}╝{colors.RESET}{colors.SHADOW}░{colors.RESET}\n"
        f"   {colors.SHADOW}{shadow_line}{colors.RESET}"
    )


def format_team(
    name: str,
    members: list[tuple[str, str]],
    colors: ColorScheme,
) -> str:
    """Format team block with members and their roles."""
    max_name = max(len(m) for m, _ in members)
    lines = [f"  {colors.TEAM}{name}:{colors.RESET}"]
    for member, role in members:
        padded = f"{member:<{max_name}}"
        lines.append(
            f"    {colors.BULLET}●{colors.RESET} {padded}"
            f"  {colors.ROLE}({role}){colors.RESET}"
        )
    return "\n".join(lines)


def _bind(func: Callable, **kwargs: Any) -> Callable:
    """Create a partial that preserves the original docstring."""
    bound = partial(func, **kwargs)
    bound.__doc__ = func.__doc__
    return bound


def bootstrap_commands(
    colors: ColorScheme,
    book: AddressBook,
    notebook: NoteBook,
) -> dict[str, Callable]:
    """Build the command registry.

    To add a new command:
      1. Define a handler in handlers/ (see README for file layout):

            @command("Description. Usage: my-cmd <arg>")
            def handle_my_cmd(*args: str, book: AddressBook) -> str:
                ...

      2. Import the handler here and register it with _bind:

            "my-cmd": _bind(handle_my_cmd, book=book),

      Dependencies like ``book``, ``notebook``, and ``colors`` are injected
      via _bind so the REPL can call every handler as ``handler(*user_args)``.
    """
    return {
        # Built-in commands
        "hello": handle_hello,
        "quit": _bind(handle_quit, colors=colors),
        "help": _bind(handle_help, colors=colors),
        # Contact commands
        "add": _bind(handle_add_contact, book=book),
        "delete": _bind(handle_delete_contact, book=book),
        "change-phone": _bind(handle_change_phone, book=book),
        "remove-phone": _bind(handle_remove_phone, book=book),
        "phone": _bind(handle_show_phone, book=book),
        "all": _bind(handle_show_all, book=book),
        "add-birthday": _bind(handle_add_birthday, book=book),
        "show-birthday": _bind(handle_show_birthday, book=book),
        "change-birthday": _bind(handle_change_birthday, book=book),
        "remove-birthday": _bind(handle_remove_birthday, book=book),
        "add-email": _bind(handle_add_email, book=book),
        "show-email": _bind(handle_show_email, book=book),
        "change-email": _bind(handle_change_email, book=book),
        "remove-email": _bind(handle_remove_email, book=book),
        "search": _bind(handle_search, book=book),
        "birthdays": _bind(handle_birthdays, book=book),
        # Note commands
        "add-note": _bind(handle_add_note, notebook=notebook),
        "delete-note": _bind(handle_delete_note, notebook=notebook),
        "edit-note": _bind(handle_edit_note, notebook=notebook),
        "search-notes": _bind(handle_search_notes, notebook=notebook),
        "all-notes": _bind(handle_show_all_notes, notebook=notebook),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=TITLE)
    parser.add_argument(
        "--no-color", action="store_true", help="disable colored output"
    )
    args = parser.parse_args(argv)

    colors = make_scheme(no_color=args.no_color or "NO_COLOR" in os.environ)
    book = load_contacts()
    notebook = load_notes()
    commands = bootstrap_commands(colors, book, notebook)

    def on_save() -> None:
        save_contacts(book)
        save_notes(notebook)

    print()
    print(format_title(TITLE, colors))
    print()
    print(format_team(TEAM_NAME, TEAM_MEMBERS, colors))
    print()
    print(handle_help(commands, colors=colors))
    print()

    run_repl(commands, colors, on_save)


if __name__ == "__main__":
    main()
