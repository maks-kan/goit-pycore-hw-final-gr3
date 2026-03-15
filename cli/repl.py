import difflib
import shlex
from collections.abc import Callable

from cli.colors import ColorScheme
from cli.commands import handle_help, handle_quit
from cli.errors import UsageError


def run_repl(
    commands: dict[str, Callable],
    colors: ColorScheme,
    book: object,
    storage: object,
) -> None:
    """Read-eval-print loop for the assistant bot.

    ``book`` must expose ``.is_changed()`` and ``storage`` must expose
    ``.save(book)`` so the REPL can persist changes automatically.
    """
    while True:
        try:
            user_input = input(">>> ").strip()
        except EOFError, KeyboardInterrupt:
            print()
            if book.is_changed():
                storage.save(book)
            print(handle_quit(colors=colors))
            break

        if not user_input:
            continue

        try:
            parts = shlex.split(user_input)
        except ValueError:
            print(f"{colors.ERROR}Invalid input: unmatched quotes.{colors.RESET}")
            continue

        cmd_name = parts[0].lower()

        if cmd_name in ("quit", "exit", "close"):
            if book.is_changed():
                storage.save(book)
            print(handle_quit(colors=colors))
            break

        if cmd_name == "help":
            print(f"\n{handle_help(commands, colors=colors)}\n")
            continue

        handler = commands.get(cmd_name)
        if handler is None:
            msg = f"Unknown command: {cmd_name}"
            matches = difflib.get_close_matches(
                cmd_name, commands.keys(), n=1, cutoff=0.6
            )
            if matches:
                msg += f". Did you mean: {matches[0]}?"
            print(f"{colors.ERROR}{msg}{colors.RESET}")
            continue

        try:
            result = handler(*parts[1:])
        except UsageError as exc:
            print(f"\n  {colors.ERROR}{exc}{colors.RESET}")
            print(f"  {colors.USAGE}{handler.__doc__}{colors.RESET}\n")
            continue
        except ValueError as exc:
            print(f"\n  {colors.ERROR}Error: {exc}{colors.RESET}\n")
            continue

        print(f"\n{result}\n")

        if book.is_changed():
            storage.save(book)
