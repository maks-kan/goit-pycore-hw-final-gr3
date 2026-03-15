from collections.abc import Callable
from typing import Any

from cli.colors import ColorScheme

__all__ = ["command", "handle_echo", "handle_greet", "handle_help", "handle_quit"]


def command(help_text: str) -> Callable[[Callable], Callable]:
    """Decorator that wraps a function and sets help_text as the wrapper's docstring."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        wrapper.__doc__ = help_text
        return wrapper

    return decorator


@command("Show available commands.")
def handle_help(commands: dict[str, Callable], *, colors: ColorScheme) -> str:
    """Format and return a help listing of all registered commands."""
    lines = [f"  {colors.HEADER}Available commands:{colors.RESET}"]
    for name, handler in sorted(commands.items()):
        colored_name = f"{colors.CMD_NAME}{name:<15}{colors.RESET}"
        colored_desc = f"{colors.CMD_DESC}{handler.__doc__}{colors.RESET}"
        lines.append(f"    {colored_name} {colored_desc}")
    return "\n".join(lines)


@command("Echo arguments back (test command).")
def handle_echo(*args: str) -> str:
    """Print all received arguments."""
    lines = [f"  {i}: {arg}" for i, arg in enumerate(args, 1)]
    return "\n".join(lines) if lines else "(no arguments)"


@command("Greet by name. Usage: greet <name>")
def handle_greet(*args: str, colors: ColorScheme) -> str:
    """Greet the given person."""
    if not args:
        raise ValueError("name is required")
    return f"  {colors.GREETING}Hello, {args[0]}!{colors.RESET}"


@command("Exit the assistant bot.")
def handle_quit(*, colors: ColorScheme) -> str:
    """Return a farewell message."""
    return f"{colors.FAREWELL}Good bye!{colors.RESET}"
