from datetime import date

import pytest

from models.fields import Birthday, Email, Field, Name, Phone


class TestField:
    def test_stores_value(self) -> None:
        assert Field("hello").value == "hello"

    def test_stores_none(self) -> None:
        assert Field(None).value is None


class TestName:
    def test_valid_name(self) -> None:
        assert Name("Alice").value == "Alice"

    def test_empty_name_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            Name("")

    def test_none_name_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            Name(None)


class TestPhone:
    def test_valid_phone(self) -> None:
        assert Phone("0501234567").value == "0501234567"

    def test_empty_phone_raises(self) -> None:
        with pytest.raises(ValueError):
            Phone("")

    def test_non_digits_raises(self) -> None:
        with pytest.raises(ValueError, match="digits"):
            Phone("050-123-45")

    def test_short_number_raises(self) -> None:
        with pytest.raises(ValueError, match="10 digits"):
            Phone("12345")

    def test_long_number_raises(self) -> None:
        with pytest.raises(ValueError, match="10 digits"):
            Phone("12345678901")

    def test_setter_validates(self) -> None:
        phone = Phone("0501234567")
        with pytest.raises(ValueError):
            phone.value = "abc"


class TestEmail:
    def test_valid_email(self) -> None:
        assert Email("alice@example.com").value == "alice@example.com"

    def test_setter_validates(self) -> None:
        email = Email("alice@example.com")
        with pytest.raises(ValueError):
            email.value = "no-at-sign"

    def test_no_at_raises(self) -> None:
        with pytest.raises(ValueError, match="email"):
            Email("alice.example.com")

    def test_starts_with_at_raises(self) -> None:
        with pytest.raises(ValueError, match="email"):
            Email("@example.com")

    def test_ends_with_at_raises(self) -> None:
        with pytest.raises(ValueError, match="email"):
            Email("alice@")

    def test_double_at_raises(self) -> None:
        with pytest.raises(ValueError, match="email"):
            Email("alice@@example.com")


class TestBirthday:
    def test_valid_date(self) -> None:
        bday = Birthday("15.03.1990")
        assert bday.value == date(1990, 3, 15)

    def test_invalid_format_raises(self) -> None:
        with pytest.raises(ValueError, match="DD.MM.YYYY"):
            Birthday("1990-03-15")

    def test_nonsense_raises(self) -> None:
        with pytest.raises(ValueError, match="DD.MM.YYYY"):
            Birthday("not-a-date")
