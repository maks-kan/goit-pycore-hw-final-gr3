import pytest

from models.address_book import AddressBook
from models.record import Record


@pytest.fixture()
def book() -> AddressBook:
    ab = AddressBook()
    ab.add_record(Record("Alice", phones=["0501234567"], email="alice@test.com"))
    ab.add_record(Record("Bob", phones=["0507654321"]))
    return ab


class TestAddRecord:
    def test_add_new_record(self) -> None:
        ab = AddressBook()
        ab.add_record(Record("Alice"))
        assert ab.get_record("Alice") is not None

    def test_add_replaces_existing(self) -> None:
        ab = AddressBook()
        old = Record("Alice", phones=["0501111111"])
        new = Record("Alice", phones=["0502222222"])
        ab.add_record(old)
        ab.add_record(new)
        assert len(ab.list_all()) == 1
        assert ab.get_record("Alice") is new


class TestGetRecord:
    def test_existing(self, book: AddressBook) -> None:
        assert book.get_record("Alice") is not None

    def test_missing_returns_none(self, book: AddressBook) -> None:
        assert book.get_record("Eve") is None


class TestDeleteRecord:
    def test_delete_existing(self, book: AddressBook) -> None:
        book.delete_record("Alice")
        assert book.get_record("Alice") is None
        assert len(book.list_all()) == 1
        assert book.get_record("Bob") is not None

    def test_delete_missing_raises(self, book: AddressBook) -> None:
        with pytest.raises(ValueError, match="not found"):
            book.delete_record("Eve")


class TestSearch:
    def test_search_by_name(self, book: AddressBook) -> None:
        results = book.search("alice")
        assert len(results) == 1
        assert results[0].name.value == "Alice"

    def test_search_by_phone(self, book: AddressBook) -> None:
        results = book.search("0507654321")
        assert len(results) == 1
        assert results[0].name.value == "Bob"

    def test_search_by_email(self, book: AddressBook) -> None:
        results = book.search("alice@test")
        assert len(results) == 1
        assert results[0].name.value == "Alice"

    def test_search_by_partial_phone(self, book: AddressBook) -> None:
        results = book.search("050")
        assert len(results) == 2

    def test_search_no_match(self, book: AddressBook) -> None:
        assert book.search("xyz") == []

    def test_search_case_insensitive(self, book: AddressBook) -> None:
        assert len(book.search("ALICE")) == 1


class TestListAll:
    def test_list_all(self, book: AddressBook) -> None:
        assert len(book.list_all()) == 2

    def test_list_all_empty(self) -> None:
        assert AddressBook().list_all() == []
