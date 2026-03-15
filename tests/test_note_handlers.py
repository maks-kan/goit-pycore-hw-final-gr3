"""Tests for handlers/note_handlers.py."""

import pytest

from cli.errors import UsageError
from handlers.note_handlers import (
    handle_add_note,
    handle_delete_note,
    handle_edit_note,
    handle_search_notes,
    handle_show_all_notes,
)
from models.notebook import NoteBook


@pytest.fixture()
def nb() -> NoteBook:
    nb = NoteBook()
    nb.add_note("First note", tags=["work"])
    nb.add_note("Second note", tags=["personal"])
    return nb


class TestAddNote:
    def test_add(self, nb: NoteBook) -> None:
        assert handle_add_note("Third", "note", notebook=nb) == "Note added."
        assert len(nb) == 3
        assert nb.notes[-1].text == "Third note"

    def test_no_args_raises(self) -> None:
        with pytest.raises(UsageError, match="text is required"):
            handle_add_note(notebook=NoteBook())


class TestDeleteNote:
    def test_delete_first(self, nb: NoteBook) -> None:
        assert handle_delete_note("1", notebook=nb) == "Note deleted."
        assert len(nb) == 1
        assert nb.notes[0].text == "Second note"

    def test_invalid_index(self, nb: NoteBook) -> None:
        result = handle_delete_note("99", notebook=nb)
        assert result == "Note not found (invalid number)."

    def test_non_integer_raises(self, nb: NoteBook) -> None:
        with pytest.raises(UsageError, match="number must be an integer"):
            handle_delete_note("abc", notebook=nb)

    def test_no_args_raises(self) -> None:
        with pytest.raises(UsageError, match="number is required"):
            handle_delete_note(notebook=NoteBook())


class TestEditNote:
    def test_edit_text(self, nb: NoteBook) -> None:
        assert handle_edit_note("1", "Updated", "text", notebook=nb) == "Note updated."
        assert nb.notes[0].text == "Updated text"

    def test_invalid_index(self, nb: NoteBook) -> None:
        result = handle_edit_note("99", "text", notebook=nb)
        assert result == "Note not found (invalid number)."

    def test_preserves_tags(self, nb: NoteBook) -> None:
        handle_edit_note("1", "New", "text", notebook=nb)
        assert nb.notes[0].tags == ["work"]

    def test_not_enough_args_raises(self) -> None:
        with pytest.raises(UsageError, match="number and new text"):
            handle_edit_note("1", notebook=NoteBook())


class TestSearchNotes:
    def test_found(self, nb: NoteBook) -> None:
        result = handle_search_notes("First", notebook=nb)
        assert "First note" in result

    def test_not_found(self, nb: NoteBook) -> None:
        assert handle_search_notes("xyz", notebook=nb) == "No notes found."

    def test_no_args_raises(self) -> None:
        with pytest.raises(UsageError, match="keyword is required"):
            handle_search_notes(notebook=NoteBook())


class TestShowAllNotes:
    def test_lists_notes(self, nb: NoteBook) -> None:
        result = handle_show_all_notes(notebook=nb)
        assert "First note" in result
        assert "Second note" in result
        assert "1." in result
        assert "2." in result

    def test_empty_notebook(self) -> None:
        assert handle_show_all_notes(notebook=NoteBook()) == "No notes saved."

    def test_with_args_raises(self, nb: NoteBook) -> None:
        with pytest.raises(UsageError, match="no arguments expected"):
            handle_show_all_notes("x", notebook=nb)
