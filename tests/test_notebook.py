import pytest

from models.note import Note
from models.notebook import NoteBook


class TestNote:
    def test_create(self) -> None:
        note = Note("Title", "hello")
        assert note.title == "Title"
        assert note.text == "hello"
        assert note.tags == []

    def test_create_with_tags(self) -> None:
        note = Note("Title", "hello", tags="work urgent")
        assert note.tags == ["work", "urgent"]

    def test_matches_title(self) -> None:
        note = Note("Groceries", "Buy milk")
        assert note.matches("groceries") is True

    def test_matches_text(self) -> None:
        note = Note("Title", "Buy groceries")
        assert note.matches("groceries") is True

    def test_matches_text_case_insensitive(self) -> None:
        note = Note("Title", "Buy groceries")
        assert note.matches("GROCERIES") is True

    def test_matches_tag(self) -> None:
        note = Note("Title", "hello", tags="work")
        assert note.matches("work") is True

    def test_matches_tag_case_insensitive(self) -> None:
        note = Note("Title", "hello", tags="Work")
        assert note.matches("WORK") is True

    def test_no_match(self) -> None:
        note = Note("Title", "hello", tags="work")
        assert note.matches("xyz") is False

    def test_repr(self) -> None:
        note = Note("Title", "hello", tags="work")
        result = repr(note)
        assert "Title" in result
        assert "hello" in result
        assert "work" in result

    def test_add_tags(self) -> None:
        note = Note("Title", "text")
        note.add_tags("work urgent")
        assert note.tags == ["work", "urgent"]

    def test_add_tags_no_duplicates(self) -> None:
        note = Note("Title", "text", tags="work")
        note.add_tags("work urgent")
        assert note.tags == ["work", "urgent"]

    def test_add_tags_invalid(self) -> None:
        note = Note("Title", "text")
        with pytest.raises(ValueError, match="Invalid tag"):
            note.add_tags("bad!tag")

    def test_remove_tag(self) -> None:
        note = Note("Title", "text", tags="work urgent")
        assert note.remove_tag("work") is True
        assert note.tags == ["urgent"]

    def test_remove_tag_not_found(self) -> None:
        note = Note("Title", "text", tags="work")
        assert note.remove_tag("missing") is False


class TestNoteBook:
    @pytest.fixture()
    def nb(self) -> NoteBook:
        nb = NoteBook()
        nb.add_note("First", "First note", tags="work")
        nb.add_note("Second", "Second note", tags="personal")
        return nb

    def test_add_note(self) -> None:
        nb = NoteBook()
        assert nb.add_note("Title", "hello") is True
        assert len(nb) == 1

    def test_add_note_duplicate_title(self) -> None:
        nb = NoteBook()
        nb.add_note("Title", "hello")
        assert nb.add_note("Title", "other") is False
        assert len(nb) == 1

    def test_add_note_with_tags(self) -> None:
        nb = NoteBook()
        nb.add_note("Title", "hello", tags="work urgent")
        assert nb.find_note_by_title("Title").tags == ["work", "urgent"]

    def test_len(self, nb: NoteBook) -> None:
        assert len(nb) == 2

    def test_find_note_by_title(self, nb: NoteBook) -> None:
        note = nb.find_note_by_title("First")
        assert note is not None
        assert note.text == "First note"

    def test_find_note_by_title_not_found(self, nb: NoteBook) -> None:
        assert nb.find_note_by_title("Missing") is None

    def test_delete_note(self, nb: NoteBook) -> None:
        assert nb.delete_note("First") is True
        assert len(nb) == 1
        assert nb.find_note_by_title("Second") is not None

    def test_delete_note_not_found(self, nb: NoteBook) -> None:
        assert nb.delete_note("Missing") is False
        assert len(nb) == 2

    def test_edit_note_text(self, nb: NoteBook) -> None:
        assert nb.edit_note("First", new_text="Updated") is True
        assert nb.find_note_by_title("First").text == "Updated"

    def test_edit_note_title(self, nb: NoteBook) -> None:
        assert nb.edit_note("First", new_title="Renamed") is True
        assert nb.find_note_by_title("Renamed") is not None
        assert nb.find_note_by_title("First") is None

    def test_edit_note_title_conflict(self, nb: NoteBook) -> None:
        assert nb.edit_note("First", new_title="Second") is False

    def test_edit_note_tags(self, nb: NoteBook) -> None:
        assert nb.edit_note("First", new_tags=["new"]) is True
        assert nb.find_note_by_title("First").tags == ["new"]

    def test_edit_note_preserves_unchanged(self, nb: NoteBook) -> None:
        original_tags = nb.find_note_by_title("First").tags.copy()
        nb.edit_note("First", new_text="Changed text only")
        assert nb.find_note_by_title("First").tags == original_tags

    def test_edit_note_not_found(self, nb: NoteBook) -> None:
        assert nb.edit_note("Missing", new_text="x") is False

    def test_search_by_text(self, nb: NoteBook) -> None:
        results = nb.search("First")
        assert len(results) == 1
        assert results[0].text == "First note"

    def test_search_by_tag(self, nb: NoteBook) -> None:
        results = nb.search("personal")
        assert len(results) == 1
        assert results[0].title == "Second"

    def test_search_no_match(self, nb: NoteBook) -> None:
        assert nb.search("xyz") == []

    def test_search_common_word(self, nb: NoteBook) -> None:
        results = nb.search("note")
        assert len(results) == 2

    def test_empty_notebook(self) -> None:
        nb = NoteBook()
        assert len(nb) == 0
        assert nb.search("anything") == []
