import argparse
import os
from collections.abc import Callable
from datetime import date, timedelta
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
    handle_add_tags,
    handle_all_tags,
    handle_delete_note,
    handle_edit_note,
    handle_notes_by_tag,
    handle_remove_tag,
    handle_rename_note,
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
        "hello": _bind(handle_hello, colors=colors),
        "quit": _bind(handle_quit, colors=colors),
        "help": _bind(handle_help, colors=colors),
        # Contact commands
        "add": _bind(handle_add_contact, book=book, colors=colors),
        "delete": _bind(handle_delete_contact, book=book, colors=colors),
        "change-phone": _bind(handle_change_phone, book=book, colors=colors),
        "delete-phone": _bind(handle_remove_phone, book=book, colors=colors),
        "phone": _bind(handle_show_phone, book=book, colors=colors),
        "all": _bind(handle_show_all, book=book, colors=colors),
        "add-birthday": _bind(handle_add_birthday, book=book, colors=colors),
        "show-birthday": _bind(handle_show_birthday, book=book, colors=colors),
        "change-birthday": _bind(handle_change_birthday, book=book, colors=colors),
        "delete-birthday": _bind(handle_remove_birthday, book=book, colors=colors),
        "add-email": _bind(handle_add_email, book=book, colors=colors),
        "show-email": _bind(handle_show_email, book=book, colors=colors),
        "change-email": _bind(handle_change_email, book=book, colors=colors),
        "delete-email": _bind(handle_remove_email, book=book, colors=colors),
        "search": _bind(handle_search, book=book, colors=colors),
        "birthdays": _bind(handle_birthdays, book=book, colors=colors),
        # Note commands
        "add-note": _bind(handle_add_note, notebook=notebook, colors=colors),
        "delete-note": _bind(handle_delete_note, notebook=notebook, colors=colors),
        "edit-note": _bind(handle_edit_note, notebook=notebook, colors=colors),
        "search-notes": _bind(handle_search_notes, notebook=notebook, colors=colors),
        "all-notes": _bind(handle_show_all_notes, notebook=notebook, colors=colors),
        "rename-note": _bind(handle_rename_note, notebook=notebook, colors=colors),
        "add-tags": _bind(handle_add_tags, notebook=notebook, colors=colors),
        "delete-tag": _bind(handle_remove_tag, notebook=notebook, colors=colors),
        "all-tags": _bind(handle_all_tags, notebook=notebook, colors=colors),
        "notes-by-tag": _bind(handle_notes_by_tag, notebook=notebook, colors=colors),
    }


def _create_demo_data() -> tuple[AddressBook, NoteBook]:
    """Create pre-populated address book and notebook with sample data."""
    today = date.today()

    def _bday(delta_days: int) -> str:
        d = today + timedelta(days=delta_days)
        return d.strftime("%d.%m.%Y")

    book = AddressBook()
    from models.record import Record

    for name, phones, email, bday in [
        ("Alice Johnson", ["0501234567", "0509876543"], "alice@example.com", _bday(3)),
        ("Bob Smith", ["0671112233"], "bob@work.com", _bday(7)),
        ("Charlie Brown", ["0931234567"], "charlie@mail.com", _bday(45)),
        ("Diana Prince", ["0661234567", "0669876543"], "diana@hero.org", _bday(180)),
        ("Eve Adams", ["0501111111"], None, _bday(1)),
        ("Frank Miller", ["0672222222"], "frank@example.com", None),
        ("Grace Lee", ["0933333333", "0934444444"], "grace@test.com", _bday(0)),
    ]:
        rec = Record(name, phones=phones, email=email, birthday=bday)
        book.add_record(rec)

    notebook = NoteBook()
    for title, text, tags in [
        ("Shopping", "Buy milk, eggs, and bread", "personal errands"),
        ("Sprint goals", "Finish auth module and write tests", "work urgent"),
        ("Book list", "Clean Code, Pragmatic Programmer", "personal reading"),
        ("Meeting notes", "Discuss API design with the team", "work"),
        ("Workout plan", "Mon: run, Wed: gym, Fri: swim", "personal health"),
        ("Project ideas", "CLI tool for note management", "work ideas"),
        ("Travel", "Plan summer vacation to Italy", None),
    ]:
        notebook.add_note(title, text, tags=tags)

    return book, notebook


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=TITLE)
    parser.add_argument(
        "--no-color", action="store_true", help="disable colored output"
    )
    parser.add_argument(
        "--demo", action="store_true", help="start with sample demo data"
    )
    args = parser.parse_args(argv)

    colors = make_scheme(no_color=args.no_color or "NO_COLOR" in os.environ)
    if args.demo:
        book, notebook = _create_demo_data()
    else:
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
