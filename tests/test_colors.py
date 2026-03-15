"""Tests for cli/colors.py — color scheme factory."""

import re

from cli.colors import ColorScheme, make_scheme

_ANSI_RE = re.compile(r"\x1b\[")


class TestMakeScheme:
    def test_plain_has_no_ansi(self) -> None:
        scheme = make_scheme(no_color=True)
        for field in ColorScheme.__dataclass_fields__:
            assert _ANSI_RE.search(getattr(scheme, field)) is None

    def test_colored_has_ansi(self) -> None:
        scheme = make_scheme(no_color=False)
        for field in ColorScheme.__dataclass_fields__:
            if field == "RESET":
                continue
            assert _ANSI_RE.search(getattr(scheme, field)) is not None

    def test_plain_fields_are_empty_strings(self) -> None:
        scheme = make_scheme(no_color=True)
        for field in ColorScheme.__dataclass_fields__:
            assert getattr(scheme, field) == ""

    def test_colored_reset_is_nonempty(self) -> None:
        scheme = make_scheme(no_color=False)
        assert scheme.RESET != ""


class TestColorScheme:
    def test_is_frozen(self) -> None:
        scheme = make_scheme(no_color=True)
        import pytest

        with pytest.raises(AttributeError):
            scheme.RESET = "x"

    def test_all_fields_present(self) -> None:
        expected = {
            "RESET",
            "TITLE",
            "SHADOW",
            "TEAM",
            "BULLET",
            "CMD_NAME",
            "CMD_DESC",
            "HEADER",
            "ERROR",
            "USAGE",
            "GREETING",
            "FAREWELL",
            "ROLE",
        }
        assert set(ColorScheme.__dataclass_fields__) == expected
