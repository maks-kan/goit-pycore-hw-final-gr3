import argparse
import os
import shlex

from cli.colors import ColorScheme, make_scheme
from cli.commands import default_commands, handle_help, handle_quit

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


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=TITLE)
    parser.add_argument(
        "--no-color", action="store_true", help="disable colored output"
    )
    args = parser.parse_args(argv)

    colors = make_scheme(no_color=args.no_color or "NO_COLOR" in os.environ)
    commands = default_commands(colors)

    print()
    print(format_title(TITLE, colors))
    print()
    print(format_team(TEAM_NAME, TEAM_MEMBERS, colors))
    print()
    print(handle_help(commands, colors=colors))
    print()

    while True:
        try:
            user_input = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
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
            print(handle_quit(colors=colors))
            break

        if cmd_name == "help":
            print(f"\n{handle_help(commands, colors=colors)}\n")
            continue

        handler = commands.get(cmd_name)
        if handler is None:
            print(f"{colors.ERROR}Unknown command: {cmd_name}{colors.RESET}")
            continue

        try:
            result = handler(*parts[1:])
        except ValueError as exc:
            print(f"\n  {colors.ERROR}Invalid input: {exc}{colors.RESET}")
            usage = f"{cmd_name} — {handler.__doc__}"
            print(f"  {colors.USAGE}Usage: {usage}{colors.RESET}\n")
            continue

        print(f"\n{result}\n")


if __name__ == "__main__":
    main()
