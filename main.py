import argparse
import os
from collections.abc import Callable
from functools import partial
from typing import Any

from cli.colors import ColorScheme, make_scheme
from cli.commands import handle_echo, handle_greet, handle_help, handle_quit
from cli.repl import run_repl


class AddressBook:
    """Stub — replace with real implementation."""

    def __init__(self) -> None:
        self._changed = False

    def is_changed(self) -> bool:
        return self._changed

    def mark_saved(self) -> None:
        self._changed = False


class Storage:
    """Stub — replace with real implementation."""

    def load(self) -> AddressBook:
        return AddressBook()

    def save(self, book: AddressBook) -> None:
        book.mark_saved()


TITLE = "Assistant Bot"
TEAM_NAME = "Team #3"
TEAM_MEMBERS = [
    "Olga Shadrunova",
    "Maks Kaniuka",
    "Ivan Bochkarov",
    "Oleksandr Semychenkov",
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


def format_team(name: str, members: list[str], colors: ColorScheme) -> str:
    """Format team block with members listed."""
    lines = [f"  {colors.TEAM}{name}:{colors.RESET}"]
    for member in members:
        lines.append(f"    {colors.BULLET}●{colors.RESET} {member}")
    return "\n".join(lines)


def _bind(func: Callable, **kwargs: Any) -> Callable:
    """Create a partial that preserves the original docstring."""
    bound = partial(func, **kwargs)
    bound.__doc__ = func.__doc__
    return bound


def bootstrap_commands(
    colors: ColorScheme, book: AddressBook,
) -> dict[str, Callable]:
    """Build the command registry.

    To add a new command:
      1. Define a handler in handlers/ (see README for file layout):

            # handlers/contact_handlers.py
            def add_contact(*args: str, book: AddressBook) -> str:
                if len(args) < 2:
                    raise ValueError("name and phone are required")
                name, phone = args[0], args[1]
                # ... add to book ...
                return f"Added {name}"

      2. Import the handler here and register it with _bind:

            from handlers.contact_handlers import add_contact
            ...
            "add": _bind(add_contact, book=book),

      Dependencies like ``book`` and ``colors`` are injected via _bind
      so the REPL can call every handler as ``handler(*user_args)``.
    """
    return {
        "echo": handle_echo,
        "greet": _bind(handle_greet, colors=colors),
        "help": _bind(handle_help, colors=colors),
        "quit": _bind(handle_quit, colors=colors),
        # Example registrations (uncomment when handlers exist):
        # "add": _bind(handle_add, book=book),
        # "show": _bind(handle_show, book=book, colors=colors),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=TITLE)
    parser.add_argument(
        "--no-color", action="store_true", help="disable colored output"
    )
    args = parser.parse_args(argv)

    colors = make_scheme(no_color=args.no_color or "NO_COLOR" in os.environ)
    storage = Storage()
    book = storage.load()
    commands = bootstrap_commands(colors, book)

    print()
    print(format_title(TITLE, colors))
    print()
    print(format_team(TEAM_NAME, TEAM_MEMBERS, colors))
    print()
    print(handle_help(commands, colors=colors))
    print()

    run_repl(commands, colors, book, storage)


if __name__ == "__main__":
    main()
