"""Tests for handlers/note_handlers.py."""

import pytest

from cli.colors import ColorScheme
from cli.errors import AlreadyExistsError, NotFoundError, UsageError
from handlers.note_handlers import (
    handle_add_note,
    handle_add_tags,
    handle_all_tags,
    handle_delete_note,
    handle_edit_note,
    handle_notes_by_tag,
    handle_remove_tag,
    handle_rename_note,
    handle_search_notes,
    handle_show_all_notes,
)
from models.notebook import NoteBook


@pytest.fixture()
def nb() -> NoteBook:
    nb = NoteBook()
    nb.add_note("Shopping", "Buy milk and eggs")
    nb.add_note("Work", "Finish the report", tags="urgent")
    return nb


class TestAddNote:
    def test_add(self, nb: NoteBook, colors: ColorScheme) -> None:
        result = handle_add_note("Ideas", "Learn", "Rust", notebook=nb, colors=colors)
        assert result == "Note 'Ideas' added."
        assert len(nb) == 3
        assert nb.notes[-1].text == "Learn Rust"

    def test_duplicate_title(self, nb: NoteBook, colors: ColorScheme) -> None:
        with pytest.raises(AlreadyExistsError, match="already exists"):
            handle_add_note("Shopping", "Other text", notebook=nb, colors=colors)

    def test_no_args_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="title and text are required"):
            handle_add_note(notebook=NoteBook(), colors=colors)

    def test_title_only_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="title and text are required"):
            handle_add_note("Title", notebook=NoteBook(), colors=colors)


class TestDeleteNote:
    def test_delete(self, nb: NoteBook, colors: ColorScheme) -> None:
        result = handle_delete_note("Shopping", notebook=nb, colors=colors)
        assert result == "Note 'Shopping' deleted."
        assert len(nb) == 1

    def test_not_found(self, nb: NoteBook, colors: ColorScheme) -> None:
        with pytest.raises(NotFoundError, match="not found"):
            handle_delete_note("Nonexistent", notebook=nb, colors=colors)

    def test_no_args_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="title is required"):
            handle_delete_note(notebook=NoteBook(), colors=colors)


class TestEditNote:
    def test_edit_text(self, nb: NoteBook, colors: ColorScheme) -> None:
        result = handle_edit_note(
            "Shopping", "Updated", "text", notebook=nb, colors=colors
        )
        assert result == "Note 'Shopping' updated."
        assert nb.find_note_by_title("Shopping").text == "Updated text"

    def test_not_found(self, nb: NoteBook, colors: ColorScheme) -> None:
        with pytest.raises(NotFoundError, match="not found"):
            handle_edit_note("Nonexistent", "text", notebook=nb, colors=colors)

    def test_preserves_tags(self, nb: NoteBook, colors: ColorScheme) -> None:
        handle_edit_note("Work", "New", "text", notebook=nb, colors=colors)
        assert nb.find_note_by_title("Work").tags == ["urgent"]

    def test_not_enough_args_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="title and new text are required"):
            handle_edit_note("Title", notebook=NoteBook(), colors=colors)


class TestRenameNote:
    def test_rename(self, nb: NoteBook, colors: ColorScheme) -> None:
        result = handle_rename_note("Shopping", "Groceries", notebook=nb, colors=colors)
        assert result == "Note 'Shopping' renamed to 'Groceries'."
        assert nb.find_note_by_title("Groceries") is not None
        assert nb.find_note_by_title("Shopping") is None

    def test_not_found(self, nb: NoteBook, colors: ColorScheme) -> None:
        with pytest.raises(NotFoundError, match="not found"):
            handle_rename_note("Nonexistent", "New", notebook=nb, colors=colors)

    def test_target_exists(self, nb: NoteBook, colors: ColorScheme) -> None:
        with pytest.raises(AlreadyExistsError, match="already exist"):
            handle_rename_note("Shopping", "Work", notebook=nb, colors=colors)

    def test_not_enough_args_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="title and new title are required"):
            handle_rename_note("Title", notebook=NoteBook(), colors=colors)


class TestAddTags:
    def test_add_tags(self, nb: NoteBook, colors: ColorScheme) -> None:
        result = handle_add_tags(
            "Shopping", "food", "weekly", notebook=nb, colors=colors
        )
        assert result == "Tags added to note 'Shopping'."
        note = nb.find_note_by_title("Shopping")
        assert "food" in note.tags
        assert "weekly" in note.tags

    def test_not_found(self, nb: NoteBook, colors: ColorScheme) -> None:
        with pytest.raises(NotFoundError, match="not found"):
            handle_add_tags("Nonexistent", "tag", notebook=nb, colors=colors)

    def test_invalid_tag(self, nb: NoteBook, colors: ColorScheme) -> None:
        with pytest.raises(ValueError, match="Invalid tag"):
            handle_add_tags("Shopping", "bad!tag", notebook=nb, colors=colors)

    def test_not_enough_args_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="title and at least one tag"):
            handle_add_tags("Title", notebook=NoteBook(), colors=colors)


class TestRemoveTag:
    def test_remove_tag(self, nb: NoteBook, colors: ColorScheme) -> None:
        result = handle_remove_tag("Work", "urgent", notebook=nb, colors=colors)
        assert result == "Tag 'urgent' removed from note 'Work'."
        assert nb.find_note_by_title("Work").tags == []

    def test_tag_not_found(self, nb: NoteBook, colors: ColorScheme) -> None:
        with pytest.raises(NotFoundError, match="not found"):
            handle_remove_tag("Work", "nonexistent", notebook=nb, colors=colors)

    def test_note_not_found(self, nb: NoteBook, colors: ColorScheme) -> None:
        with pytest.raises(NotFoundError, match="not found"):
            handle_remove_tag("Nonexistent", "tag", notebook=nb, colors=colors)

    def test_not_enough_args_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="title and tag are required"):
            handle_remove_tag("Title", notebook=NoteBook(), colors=colors)


class TestSearchNotes:
    def test_found(self, nb: NoteBook, colors: ColorScheme) -> None:
        result = handle_search_notes("milk", notebook=nb, colors=colors)
        assert "Shopping" in result

    def test_not_found(self, nb: NoteBook, colors: ColorScheme) -> None:
        result = handle_search_notes("xyz", notebook=nb, colors=colors)
        assert result == "No notes found."

    def test_no_args_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="keyword is required"):
            handle_search_notes(notebook=NoteBook(), colors=colors)


class TestAllTags:
    def test_lists_tags_sorted(self, colors: ColorScheme) -> None:
        nb = NoteBook()
        nb.add_note("A", "text", tags="zebra alpha")
        nb.add_note("B", "text", tags="beta alpha")
        result = handle_all_tags(notebook=nb, colors=colors)
        assert result == "alpha, beta, zebra"

    def test_empty_notebook(self, colors: ColorScheme) -> None:
        result = handle_all_tags(notebook=NoteBook(), colors=colors)
        assert result == "No tags found."

    def test_no_tags(self, colors: ColorScheme) -> None:
        nb = NoteBook()
        nb.add_note("A", "text")
        result = handle_all_tags(notebook=nb, colors=colors)
        assert result == "No tags found."

    def test_with_args_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="no arguments expected"):
            handle_all_tags("x", notebook=NoteBook(), colors=colors)


class TestNotesByTag:
    def test_groups_by_tag(self, colors: ColorScheme) -> None:
        nb = NoteBook()
        nb.add_note("B", "b-text", tags="work")
        nb.add_note("A", "a-text", tags="work personal")
        nb.add_note("C", "c-text")
        result = handle_notes_by_tag(notebook=nb, colors=colors)
        lines = [ln for ln in result.splitlines() if ln]  # skip blank separators
        # Tags sorted: personal, work, then untagged
        assert "personal" in lines[0]
        assert "A: a-text" in lines[1]
        assert "work" in lines[2]
        # Notes within work sorted: A, B
        assert "A: a-text" in lines[3]
        assert "B: b-text" in lines[4]
        assert "untagged" in lines[5]
        assert "C: c-text" in lines[6]
        # All tag header lines have equal visible width
        headers = [ln for ln in result.splitlines() if ln.startswith("──")]
        stripped = [len(ln.strip()) for ln in headers]
        assert len(set(stripped)) == 1

    def test_empty_notebook(self, colors: ColorScheme) -> None:
        result = handle_notes_by_tag(notebook=NoteBook(), colors=colors)
        assert result == "No notes saved."

    def test_with_args_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="no arguments expected"):
            handle_notes_by_tag("x", notebook=NoteBook(), colors=colors)


class TestShowAllNotes:
    def test_lists_notes(self, nb: NoteBook, colors: ColorScheme) -> None:
        result = handle_show_all_notes(notebook=nb, colors=colors)
        assert "Shopping" in result
        assert "Work" in result
        lines = result.splitlines()
        assert lines[0].startswith("Title")
        assert "─" in lines[1]

    def test_empty_notebook(self, colors: ColorScheme) -> None:
        result = handle_show_all_notes(notebook=NoteBook(), colors=colors)
        assert result == "No notes saved."

    def test_with_args_raises(self, nb: NoteBook, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="no arguments expected"):
            handle_show_all_notes("x", notebook=nb, colors=colors)
