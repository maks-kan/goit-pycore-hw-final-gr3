"""Tests for storage.py — save/load notes."""

import json
from pathlib import Path

from models.notebook import NoteBook
from storage import load_notes, save_notes


class TestSaveNotes:
    def test_creates_file(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr("storage.NOTES_FILE", str(tmp_path / "notes.json"))
        nb = NoteBook()
        nb.add_note("hello")
        save_notes(nb)
        assert (tmp_path / "notes.json").exists()

    def test_writes_valid_json(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr("storage.NOTES_FILE", str(tmp_path / "notes.json"))
        nb = NoteBook()
        nb.add_note("hello", tags=["a", "b"])
        save_notes(nb)

        data = json.loads((tmp_path / "notes.json").read_text(encoding="utf-8"))
        assert len(data) == 1
        assert data[0]["text"] == "hello"
        assert data[0]["tags"] == ["a", "b"]

    def test_multiple_notes(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr("storage.NOTES_FILE", str(tmp_path / "notes.json"))
        nb = NoteBook()
        nb.add_note("first")
        nb.add_note("second", tags=["x"])
        save_notes(nb)

        data = json.loads((tmp_path / "notes.json").read_text(encoding="utf-8"))
        assert len(data) == 2

    def test_empty_notebook(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr("storage.NOTES_FILE", str(tmp_path / "notes.json"))
        save_notes(NoteBook())

        data = json.loads((tmp_path / "notes.json").read_text(encoding="utf-8"))
        assert data == []


class TestLoadNotes:
    def test_missing_file_returns_empty(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr("storage.NOTES_FILE", str(tmp_path / "nonexistent.json"))
        nb = load_notes()
        assert len(nb) == 0

    def test_roundtrip(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr("storage.NOTES_FILE", str(tmp_path / "notes.json"))
        nb = NoteBook()
        nb.add_note("Buy milk", tags=["shopping"])
        nb.add_note("Call Alice")
        save_notes(nb)

        loaded = load_notes()
        assert len(loaded) == 2
        assert loaded.notes[0].text == "Buy milk"
        assert loaded.notes[0].tags == ["shopping"]
        assert loaded.notes[1].text == "Call Alice"
        assert loaded.notes[1].tags == []

    def test_preserves_unicode(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr("storage.NOTES_FILE", str(tmp_path / "notes.json"))
        nb = NoteBook()
        nb.add_note("Привіт світ", tags=["тест"])
        save_notes(nb)

        loaded = load_notes()
        assert loaded.notes[0].text == "Привіт світ"
        assert loaded.notes[0].tags == ["тест"]
