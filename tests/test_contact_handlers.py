"""Tests for handlers/contact_handlers.py."""

import pytest

from cli.colors import ColorScheme
from cli.errors import AlreadyExistsError, NotFoundError, UsageError
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
    def test_add_new(self, book: AddressBook, colors: ColorScheme) -> None:
        result = handle_add_contact("Bob", "0509999999", book=book, colors=colors)
        assert result == "Contact added."
        assert book.get_record("Bob") is not None

    def test_add_phone_to_existing(
        self, book: AddressBook, colors: ColorScheme
    ) -> None:
        result = handle_add_contact("Alice", "0507777777", book=book, colors=colors)
        assert result == "Contact updated."
        assert len(book.get_record("Alice").phones) == 2

    def test_add_duplicate_phone(self, book: AddressBook, colors: ColorScheme) -> None:
        with pytest.raises(AlreadyExistsError, match="Phone already exists"):
            handle_add_contact("Alice", "0501234567", book=book, colors=colors)

    def test_no_args_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="name and phone"):
            handle_add_contact(book=AddressBook(), colors=colors)

    def test_one_arg_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="name and phone"):
            handle_add_contact("Alice", book=AddressBook(), colors=colors)


class TestDeleteContact:
    def test_delete_existing(self, book: AddressBook, colors: ColorScheme) -> None:
        assert (
            handle_delete_contact("Alice", book=book, colors=colors)
            == "Contact deleted."
        )
        assert book.get_record("Alice") is None

    def test_delete_missing(self, book: AddressBook, colors: ColorScheme) -> None:
        with pytest.raises(NotFoundError, match="not found"):
            handle_delete_contact("Nobody", book=book, colors=colors)

    def test_no_args_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="name is required"):
            handle_delete_contact(book=AddressBook(), colors=colors)


class TestChangePhone:
    def test_change(self, book: AddressBook, colors: ColorScheme) -> None:
        result = handle_change_phone(
            "Alice", "0501234567", "0509999999", book=book, colors=colors
        )
        assert result == "Phone updated."
        assert book.get_record("Alice").phones[0].value == "0509999999"

    def test_missing_contact(self, book: AddressBook, colors: ColorScheme) -> None:
        with pytest.raises(NotFoundError, match="not found"):
            handle_change_phone(
                "Nobody", "0501234567", "0509999999", book=book, colors=colors
            )

    def test_not_enough_args(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError):
            handle_change_phone(
                "Alice", "0501234567", book=AddressBook(), colors=colors
            )


class TestRemovePhone:
    def test_remove(self, book: AddressBook, colors: ColorScheme) -> None:
        result = handle_remove_phone("Alice", "0501234567", book=book, colors=colors)
        assert result == "Phone removed."
        assert book.get_record("Alice").phones == []

    def test_missing_contact(self, book: AddressBook, colors: ColorScheme) -> None:
        with pytest.raises(NotFoundError, match="not found"):
            handle_remove_phone("Nobody", "0501234567", book=book, colors=colors)


class TestShowPhone:
    def test_show(self, book: AddressBook, colors: ColorScheme) -> None:
        assert handle_show_phone("Alice", book=book, colors=colors) == "0501234567"

    def test_no_phones(self, book: AddressBook, colors: ColorScheme) -> None:
        book.add_record(Record("Bob"))
        result = handle_show_phone("Bob", book=book, colors=colors)
        assert result == "No phone numbers for this contact."

    def test_missing_contact(self, book: AddressBook, colors: ColorScheme) -> None:
        with pytest.raises(NotFoundError, match="not found"):
            handle_show_phone("Nobody", book=book, colors=colors)


class TestShowAll:
    def test_lists_contacts(self, book: AddressBook, colors: ColorScheme) -> None:
        result = handle_show_all(book=book, colors=colors)
        assert "Alice" in result
        lines = result.splitlines()
        assert lines[0].startswith("Name")
        assert "─" in lines[1]

    def test_empty_book(self, colors: ColorScheme) -> None:
        assert (
            handle_show_all(book=AddressBook(), colors=colors) == "No contacts saved."
        )

    def test_with_args_raises(self, book: AddressBook, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="no arguments expected"):
            handle_show_all("extra", book=book, colors=colors)


class TestBirthday:
    def test_add_birthday(self, book: AddressBook, colors: ColorScheme) -> None:
        result = handle_add_birthday("Alice", "15.03.1990", book=book, colors=colors)
        assert result == "Birthday added."

    def test_show_birthday(self, book: AddressBook, colors: ColorScheme) -> None:
        handle_add_birthday("Alice", "15.03.1990", book=book, colors=colors)
        assert handle_show_birthday("Alice", book=book, colors=colors) == "15.03.1990"

    def test_show_birthday_not_set(
        self, book: AddressBook, colors: ColorScheme
    ) -> None:
        with pytest.raises(NotFoundError, match="Birthday not set"):
            handle_show_birthday("Alice", book=book, colors=colors)

    def test_change_birthday(self, book: AddressBook, colors: ColorScheme) -> None:
        handle_add_birthday("Alice", "15.03.1990", book=book, colors=colors)
        handle_change_birthday("Alice", "25.12.2000", book=book, colors=colors)
        assert handle_show_birthday("Alice", book=book, colors=colors) == "25.12.2000"

    def test_remove_birthday(self, book: AddressBook, colors: ColorScheme) -> None:
        handle_add_birthday("Alice", "15.03.1990", book=book, colors=colors)
        result = handle_remove_birthday("Alice", book=book, colors=colors)
        assert result == "Birthday removed."
        with pytest.raises(NotFoundError, match="Birthday not set"):
            handle_show_birthday("Alice", book=book, colors=colors)

    def test_missing_contact(self, book: AddressBook, colors: ColorScheme) -> None:
        with pytest.raises(NotFoundError, match="not found"):
            handle_add_birthday("Nobody", "15.03.1990", book=book, colors=colors)


class TestEmail:
    def test_add_email(self, book: AddressBook, colors: ColorScheme) -> None:
        result = handle_add_email("Alice", "a@b.com", book=book, colors=colors)
        assert result == "Email added."

    def test_show_email(self, book: AddressBook, colors: ColorScheme) -> None:
        handle_add_email("Alice", "a@b.com", book=book, colors=colors)
        assert handle_show_email("Alice", book=book, colors=colors) == "a@b.com"

    def test_show_email_not_set(self, book: AddressBook, colors: ColorScheme) -> None:
        with pytest.raises(NotFoundError, match="Email not set"):
            handle_show_email("Alice", book=book, colors=colors)

    def test_change_email(self, book: AddressBook, colors: ColorScheme) -> None:
        handle_add_email("Alice", "a@b.com", book=book, colors=colors)
        handle_change_email("Alice", "new@b.com", book=book, colors=colors)
        assert handle_show_email("Alice", book=book, colors=colors) == "new@b.com"

    def test_remove_email(self, book: AddressBook, colors: ColorScheme) -> None:
        handle_add_email("Alice", "a@b.com", book=book, colors=colors)
        result = handle_remove_email("Alice", book=book, colors=colors)
        assert result == "Email removed."
        with pytest.raises(NotFoundError, match="Email not set"):
            handle_show_email("Alice", book=book, colors=colors)


class TestSearch:
    def test_found(self, book: AddressBook, colors: ColorScheme) -> None:
        result = handle_search("Alice", book=book, colors=colors)
        assert "Alice" in result

    def test_not_found(self, book: AddressBook, colors: ColorScheme) -> None:
        result = handle_search("Nobody", book=book, colors=colors)
        assert result == "No contacts found."


class TestBirthdays:
    def test_no_upcoming(self, book: AddressBook, colors: ColorScheme) -> None:
        result = handle_birthdays(book=book, colors=colors)
        assert result == "No birthdays in the next 7 days."

    def test_with_args_raises(self, colors: ColorScheme) -> None:
        with pytest.raises(UsageError, match="no arguments expected"):
            handle_birthdays("x", book=AddressBook(), colors=colors)
