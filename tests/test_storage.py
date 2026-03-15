"""Tests for storage.py — save/load contacts and notes."""

import json

import storage as storage_mod
from models.address_book import AddressBook
from models.notebook import NoteBook
from models.record import Record
from storage import (
    load_contacts,
    load_notes,
    save_contacts,
    save_notes,
)

# ── Contacts ────────────────────────────────────────────────────────


class TestSaveContacts:
    def test_creates_file(self) -> None:
        book = AddressBook()
        book.add_record(Record("Alice", phones=["1234567890"]))
        save_contacts(book)
        assert storage_mod.CONTACTS_FILE.exists()

    def test_writes_valid_json(self) -> None:
        book = AddressBook()
        book.add_record(Record("Alice", phones=["1234567890"], email="a@b.c"))
        save_contacts(book)

        data = json.loads(storage_mod.CONTACTS_FILE.read_text(encoding="utf-8"))
        assert len(data) == 1
        assert data[0]["name"] == "Alice"
        assert data[0]["phones"] == ["1234567890"]
        assert data[0]["email"] == "a@b.c"

    def test_empty_book(self) -> None:
        save_contacts(AddressBook())
        data = json.loads(storage_mod.CONTACTS_FILE.read_text(encoding="utf-8"))
        assert data == []

    def test_birthday_serialized(self) -> None:
        book = AddressBook()
        book.add_record(Record("Bob", birthday="15.03.2000"))
        save_contacts(book)

        data = json.loads(storage_mod.CONTACTS_FILE.read_text(encoding="utf-8"))
        assert data[0]["birthday"] == "15.03.2000"


class TestLoadContacts:
    def test_missing_file_returns_empty(self) -> None:
        book = load_contacts()
        assert book.list_all() == []

    def test_roundtrip(self) -> None:
        book = AddressBook()
        book.add_record(
            Record("Alice", phones=["1234567890"], email="a@b.c", birthday="01.01.1990")
        )
        book.add_record(Record("Bob", phones=["0987654321"]))
        save_contacts(book)

        loaded = load_contacts()
        records = {r.name.value: r for r in loaded.list_all()}
        assert len(records) == 2

        alice = records["Alice"]
        assert [p.value for p in alice.phones] == ["1234567890"]
        assert alice.email.value == "a@b.c"
        assert alice.birthday.value.strftime("%d.%m.%Y") == "01.01.1990"

        bob = records["Bob"]
        assert [p.value for p in bob.phones] == ["0987654321"]
        assert bob.email is None
        assert bob.birthday is None

    def test_preserves_unicode(self) -> None:
        book = AddressBook()
        book.add_record(Record("Олексій", phones=["1234567890"]))
        save_contacts(book)

        loaded = load_contacts()
        assert loaded.list_all()[0].name.value == "Олексій"

    def test_corrupt_json_returns_empty(self) -> None:
        storage_mod.CONTACTS_FILE.write_text("not json", encoding="utf-8")
        book = load_contacts()
        assert book.list_all() == []


# ── Notes ───────────────────────────────────────────────────────────


class TestSaveNotes:
    def test_creates_file(self) -> None:
        nb = NoteBook()
        nb.add_note("hello")
        save_notes(nb)
        assert storage_mod.NOTES_FILE.exists()

    def test_writes_valid_json(self) -> None:
        nb = NoteBook()
        nb.add_note("hello", tags=["a", "b"])
        save_notes(nb)

        data = json.loads(storage_mod.NOTES_FILE.read_text(encoding="utf-8"))
        assert len(data) == 1
        assert data[0]["text"] == "hello"
        assert data[0]["tags"] == ["a", "b"]

    def test_multiple_notes(self) -> None:
        nb = NoteBook()
        nb.add_note("first")
        nb.add_note("second", tags=["x"])
        save_notes(nb)

        data = json.loads(storage_mod.NOTES_FILE.read_text(encoding="utf-8"))
        assert len(data) == 2

    def test_empty_notebook(self) -> None:
        save_notes(NoteBook())
        data = json.loads(storage_mod.NOTES_FILE.read_text(encoding="utf-8"))
        assert data == []


class TestLoadNotes:
    def test_missing_file_returns_empty(self) -> None:
        nb = load_notes()
        assert len(nb) == 0

    def test_roundtrip(self) -> None:
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

    def test_preserves_unicode(self) -> None:
        nb = NoteBook()
        nb.add_note("Привіт світ", tags=["тест"])
        save_notes(nb)

        loaded = load_notes()
        assert loaded.notes[0].text == "Привіт світ"
        assert loaded.notes[0].tags == ["тест"]

    def test_corrupt_json_returns_empty(self) -> None:
        storage_mod.NOTES_FILE.write_text("{bad", encoding="utf-8")
        nb = load_notes()
        assert len(nb) == 0
