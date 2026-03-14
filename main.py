import shlex

from cli.commands import default_commands, handle_help, handle_quit

TITLE = "Assistant Bot"
TEAM_NAME = "Team #3"
TEAM_MEMBERS = [
    "Olga Shadrunova",
    "Maks Kaniuka",
    "Ivan Bochkarov",
    "Oleksandr Semychenkov",
]


def format_title(title: str) -> str:
    """Format title in a Unicode box with shadow."""
    width = len(title) + 4
    return (
        f"  ╔{'═' * width}╗\n"
        f"  ║  {title}  ║░\n"
        f"  ╚{'═' * width}╝░\n"
        f"   {'░' * (width + 2)}"
    )


def format_team(name: str, members: list[str]) -> str:
    """Format team block with members listed."""
    lines = [f"  {name}:"]
    for member in members:
        lines.append(f"    ● {member}")
    return "\n".join(lines)


def main() -> None:
    commands = default_commands()

    print()
    print(format_title(TITLE))
    print()
    print(format_team(TEAM_NAME, TEAM_MEMBERS))
    print()
    print(handle_help(commands))
    print()

    while True:
        try:
            user_input = input(">>> ").strip()
        except EOFError, KeyboardInterrupt:
            print()
            print(handle_quit())
            break

        if not user_input:
            continue

        try:
            parts = shlex.split(user_input)
        except ValueError:
            print("Invalid input: unmatched quotes.")
            continue

        cmd_name = parts[0].lower()

        if cmd_name in ("quit", "exit", "close"):
            print(handle_quit())
            break

        if cmd_name == "help":
            print(handle_help(commands))
            continue

        handler = commands.get(cmd_name)
        if handler is None:
            print(f"Unknown command: {cmd_name}")
            continue

        print(handler(*parts[1:]))


if __name__ == "__main__":
    main()
