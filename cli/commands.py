from collections.abc import Callable
from typing import Any


def command(help_text: str) -> Callable[[Callable], Callable]:
    """Decorator that wraps a function and sets help_text as the wrapper's docstring."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        wrapper.__doc__ = help_text
        return wrapper

    return decorator


@command("Show available commands.")
def handle_help(commands: dict[str, Callable]) -> str:
    """Format and return a help listing of all registered commands."""
    lines = ["  Available commands:"]
    for name, handler in sorted(commands.items()):
        lines.append(f"    {name:<15} {handler.__doc__}")
    return "\n".join(lines)


@command("Echo arguments back (test command).")
def handle_echo(*args: str) -> str:
    """Print all received arguments."""
    lines = [f"  {i}: {arg}" for i, arg in enumerate(args, 1)]
    return "\n".join(lines) if lines else "(no arguments)"


@command("Exit the assistant bot.")
def handle_quit() -> str:
    """Return a farewell message."""
    return "Good bye!"


def default_commands() -> dict[str, Callable]:
    """Default command registry."""
    return {
        "echo": handle_echo,
        "help": handle_help,
        "quit": handle_quit,
    }
