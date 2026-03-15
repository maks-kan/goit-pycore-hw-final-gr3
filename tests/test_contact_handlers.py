"""Tests for handlers/contact_handlers.py."""

import pytest

from cli.errors import UsageError
from handlers.contact_handlers import (
    handle_add_birthday,
    handle_add_contact,
    handle_add_email,
    handle_birthdays,
    handle_change_birthday,
    handle_change_email,
    handle_change_phone,
    handle_delete_contact,
    handle_remove_birthday,
    handle_remove_email,
    handle_remove_phone,
    handle_search,
    handle_show_all,
    handle_show_birthday,
    handle_show_email,
    handle_show_phone,
)
from models.address_book import AddressBook
from models.record import Record


@pytest.fixture()
def book() -> AddressBook:
    ab = AddressBook()
    rec = Record("Alice", phones=["0501234567"])
    ab.add_record(rec)
    return ab


class TestAddContact:
    def test_add_new(self, book: AddressBook) -> None:
        assert handle_add_contact("Bob", "0509999999", book=book) == "Contact added."
        assert book.get_record("Bob") is not None

    def test_add_phone_to_existing(self, book: AddressBook) -> None:
        result = handle_add_contact("Alice", "0507777777", book=book)
        assert result == "Contact updated."
        assert len(book.get_record("Alice").phones) == 2

    def test_add_duplicate_phone(self, book: AddressBook) -> None:
        assert (
            handle_add_contact("Alice", "0501234567", book=book)
            == "Phone already exists."
        )

    def test_no_args_raises(self) -> None:
        with pytest.raises(UsageError, match="name and phone"):
            handle_add_contact(book=AddressBook())

    def test_one_arg_raises(self) -> None:
        with pytest.raises(UsageError, match="name and phone"):
            handle_add_contact("Alice", book=AddressBook())


class TestDeleteContact:
    def test_delete_existing(self, book: AddressBook) -> None:
        assert handle_delete_contact("Alice", book=book) == "Contact deleted."
        assert book.get_record("Alice") is None

    def test_delete_missing(self, book: AddressBook) -> None:
        assert handle_delete_contact("Nobody", book=book) == "Contact not found."

    def test_no_args_raises(self) -> None:
        with pytest.raises(UsageError, match="name is required"):
            handle_delete_contact(book=AddressBook())


class TestChangePhone:
    def test_change(self, book: AddressBook) -> None:
        result = handle_change_phone("Alice", "0501234567", "0509999999", book=book)
        assert result == "Phone updated."
        assert book.get_record("Alice").phones[0].value == "0509999999"

    def test_missing_contact(self, book: AddressBook) -> None:
        result = handle_change_phone("Nobody", "0501234567", "0509999999", book=book)
        assert result == "Contact not found."

    def test_not_enough_args(self) -> None:
        with pytest.raises(UsageError):
            handle_change_phone("Alice", "0501234567", book=AddressBook())


class TestRemovePhone:
    def test_remove(self, book: AddressBook) -> None:
        assert handle_remove_phone("Alice", "0501234567", book=book) == "Phone removed."
        assert book.get_record("Alice").phones == []

    def test_missing_contact(self, book: AddressBook) -> None:
        assert (
            handle_remove_phone("Nobody", "0501234567", book=book)
            == "Contact not found."
        )


class TestShowPhone:
    def test_show(self, book: AddressBook) -> None:
        assert handle_show_phone("Alice", book=book) == "0501234567"

    def test_no_phones(self, book: AddressBook) -> None:
        book.add_record(Record("Bob"))
        assert (
            handle_show_phone("Bob", book=book) == "No phone numbers for this contact."
        )

    def test_missing_contact(self, book: AddressBook) -> None:
        assert handle_show_phone("Nobody", book=book) == "Contact not found."


class TestShowAll:
    def test_lists_contacts(self, book: AddressBook) -> None:
        result = handle_show_all(book=book)
        assert "Alice" in result

    def test_empty_book(self) -> None:
        assert handle_show_all(book=AddressBook()) == "No contacts saved."

    def test_with_args_raises(self, book: AddressBook) -> None:
        with pytest.raises(UsageError, match="no arguments expected"):
            handle_show_all("extra", book=book)


class TestBirthday:
    def test_add_birthday(self, book: AddressBook) -> None:
        result = handle_add_birthday("Alice", "15.03.1990", book=book)
        assert result == "Birthday added."

    def test_show_birthday(self, book: AddressBook) -> None:
        handle_add_birthday("Alice", "15.03.1990", book=book)
        assert handle_show_birthday("Alice", book=book) == "15.03.1990"

    def test_show_birthday_not_set(self, book: AddressBook) -> None:
        assert handle_show_birthday("Alice", book=book) == "Birthday not set."

    def test_change_birthday(self, book: AddressBook) -> None:
        handle_add_birthday("Alice", "15.03.1990", book=book)
        handle_change_birthday("Alice", "25.12.2000", book=book)
        assert handle_show_birthday("Alice", book=book) == "25.12.2000"

    def test_remove_birthday(self, book: AddressBook) -> None:
        handle_add_birthday("Alice", "15.03.1990", book=book)
        assert handle_remove_birthday("Alice", book=book) == "Birthday removed."
        assert handle_show_birthday("Alice", book=book) == "Birthday not set."

    def test_missing_contact(self, book: AddressBook) -> None:
        assert (
            handle_add_birthday("Nobody", "15.03.1990", book=book)
            == "Contact not found."
        )


class TestEmail:
    def test_add_email(self, book: AddressBook) -> None:
        assert handle_add_email("Alice", "a@b.com", book=book) == "Email added."

    def test_show_email(self, book: AddressBook) -> None:
        handle_add_email("Alice", "a@b.com", book=book)
        assert handle_show_email("Alice", book=book) == "a@b.com"

    def test_show_email_not_set(self, book: AddressBook) -> None:
        assert handle_show_email("Alice", book=book) == "Email not set."

    def test_change_email(self, book: AddressBook) -> None:
        handle_add_email("Alice", "a@b.com", book=book)
        handle_change_email("Alice", "new@b.com", book=book)
        assert handle_show_email("Alice", book=book) == "new@b.com"

    def test_remove_email(self, book: AddressBook) -> None:
        handle_add_email("Alice", "a@b.com", book=book)
        assert handle_remove_email("Alice", book=book) == "Email removed."
        assert handle_show_email("Alice", book=book) == "Email not set."


class TestSearch:
    def test_found(self, book: AddressBook) -> None:
        result = handle_search("Alice", book=book)
        assert "Alice" in result

    def test_not_found(self, book: AddressBook) -> None:
        assert handle_search("Nobody", book=book) == "No contacts found."


class TestBirthdays:
    def test_no_upcoming(self, book: AddressBook) -> None:
        assert handle_birthdays(book=book) == "No birthdays in the next 7 days."

    def test_with_args_raises(self) -> None:
        with pytest.raises(UsageError, match="no arguments expected"):
            handle_birthdays("x", book=AddressBook())
