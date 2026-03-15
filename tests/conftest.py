"""Shared test configuration."""

from pathlib import Path

import pytest

from cli.colors import make_scheme


@pytest.fixture(autouse=True)
def _isolate_storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Redirect storage files to tmp_path so tests never touch the real disk."""
    monkeypatch.setattr("storage.CONTACTS_FILE", tmp_path / "contacts.json")
    monkeypatch.setattr("storage.NOTES_FILE", tmp_path / "notes.json")


@pytest.fixture()
def colors() -> "ColorScheme":  # noqa: F821
    """Plain (no-ANSI) color scheme for handler tests."""
    return make_scheme(no_color=True)
