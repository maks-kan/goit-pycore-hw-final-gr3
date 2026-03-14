from dataclasses import dataclass

from colorama import Fore, Style, init


@dataclass(frozen=True)
class ColorScheme:
    """Immutable set of ANSI color codes used throughout the CLI."""

    RESET: str
    TITLE: str
    SHADOW: str
    TEAM: str
    BULLET: str
    CMD_NAME: str
    CMD_DESC: str
    HEADER: str
    ERROR: str
    USAGE: str
    GREETING: str
    FAREWELL: str
    ROLE: str


_COLORED = ColorScheme(
    RESET=Style.RESET_ALL,
    TITLE=Fore.CYAN + Style.BRIGHT,
    SHADOW=Style.DIM,
    TEAM=Fore.GREEN,
    BULLET=Fore.YELLOW,
    CMD_NAME=Fore.CYAN,
    CMD_DESC=Fore.WHITE,
    HEADER=Fore.MAGENTA + Style.BRIGHT,
    ERROR=Fore.RED,
    USAGE=Fore.YELLOW,
    GREETING=Fore.GREEN + Style.BRIGHT,
    FAREWELL=Fore.GREEN + Style.BRIGHT,
    ROLE=Style.DIM,
)

_PLAIN = ColorScheme(
    RESET="",
    TITLE="",
    SHADOW="",
    TEAM="",
    BULLET="",
    CMD_NAME="",
    CMD_DESC="",
    HEADER="",
    ERROR="",
    USAGE="",
    GREETING="",
    FAREWELL="",
    ROLE="",
)


def make_scheme(*, no_color: bool) -> ColorScheme:
    """Return a colored or plain scheme and initialise colorama accordingly."""
    init(strip=no_color)
    return _PLAIN if no_color else _COLORED
