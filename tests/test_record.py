from datetime import date

import pytest

from models.record import Record


class TestRecordCreation:
    def test_minimal_record(self) -> None:
        rec = Record("Alice")
        assert rec.name.value == "Alice"
        assert rec.phones == []
        assert rec.email is None
        assert rec.birthday is None

    def test_record_with_phones(self) -> None:
        rec = Record("Alice", phones=["0501234567", "0507654321"])
        assert len(rec.phones) == 2

    def test_record_with_email(self) -> None:
        rec = Record("Alice", email="alice@example.com")
        assert rec.email.value == "alice@example.com"

    def test_record_with_birthday(self) -> None:
        rec = Record("Alice", birthday="15.03.1990")
        assert rec.birthday.value.year == 1990

    def test_duplicate_phones_ignored(self) -> None:
        rec = Record("Alice", phones=["0501234567", "0501234567"])
        assert len(rec.phones) == 1


class TestRecordPhones:
    def test_add_phone(self) -> None:
        rec = Record("Alice")
        assert rec.add_phone("0501234567") is True
        assert len(rec.phones) == 1

    def test_add_invalid_phone_raises(self) -> None:
        rec = Record("Alice")
        with pytest.raises(ValueError):
            rec.add_phone("abc")

    def test_add_duplicate_phone_returns_false(self) -> None:
        rec = Record("Alice", phones=["0501234567"])
        assert rec.add_phone("0501234567") is False

    def test_remove_phone(self) -> None:
        rec = Record("Alice", phones=["0501234567"])
        assert rec.remove_phone("0501234567") is True
        assert rec.phones == []

    def test_remove_missing_phone_raises(self) -> None:
        rec = Record("Alice")
        with pytest.raises(ValueError, match="not found"):
            rec.remove_phone("0501234567")

    def test_edit_phone(self) -> None:
        rec = Record("Alice", phones=["0501234567"])
        rec.edit_phone("0501234567", "0509999999")
        assert len(rec.phones) == 1
        assert rec.phones[0].value == "0509999999"

    def test_edit_phone_preserves_others(self) -> None:
        rec = Record("Alice", phones=["0501111111", "0502222222", "0503333333"])
        rec.edit_phone("0502222222", "0509999999")
        values = [p.value for p in rec.phones]
        assert "0501111111" in values
        assert "0509999999" in values
        assert "0503333333" in values
        assert "0502222222" not in values

    def test_edit_missing_phone_raises(self) -> None:
        rec = Record("Alice")
        with pytest.raises(ValueError, match="not found"):
            rec.edit_phone("0501234567", "0509999999")


class TestRecordEmail:
    def test_edit_email(self) -> None:
        rec = Record("Alice")
        rec.edit_email("alice@new.com")
        assert rec.email.value == "alice@new.com"

    def test_edit_email_replaces(self) -> None:
        rec = Record("Alice", email="old@example.com")
        rec.edit_email("new@example.com")
        assert rec.email.value == "new@example.com"


class TestRecordBirthday:
    def test_edit_birthday(self) -> None:
        rec = Record("Alice")
        rec.edit_birthday("25.12.2000")
        assert rec.birthday.value.month == 12

    def test_days_to_birthday_no_birthday(self) -> None:
        rec = Record("Alice")
        assert rec.days_to_birthday(date(2026, 3, 16)) is None

    def test_days_to_birthday_today(self) -> None:
        rec = Record("Alice", birthday="16.03.1990")
        assert rec.days_to_birthday(date(2026, 3, 16)) == 0

    def test_days_to_birthday_tomorrow(self) -> None:
        rec = Record("Alice", birthday="17.03.1990")
        assert rec.days_to_birthday(date(2026, 3, 16)) == 1

    def test_days_to_birthday_yesterday_wraps_to_next_year(self) -> None:
        rec = Record("Alice", birthday="15.03.1990")
        result = rec.days_to_birthday(date(2026, 3, 16))
        assert result == 364

    def test_days_to_birthday_feb_29_in_leap_year(self) -> None:
        rec = Record("Alice", birthday="29.02.2000")
        # 2028 is a leap year; today is 2028-01-15 → Feb 29 is 45 days away
        assert rec.days_to_birthday(date(2028, 1, 15)) == 45

    def test_days_to_birthday_feb_29_in_non_leap_year(self) -> None:
        rec = Record("Alice", birthday="29.02.2000")
        # 2027 is not a leap year; today is 2027-01-15 → falls back to Feb 28 = 44 days
        assert rec.days_to_birthday(date(2027, 1, 15)) == 44

    def test_days_to_birthday_feb_29_past_in_non_leap_year(self) -> None:
        rec = Record("Alice", birthday="29.02.2000")
        # 2027-03-01: Feb 28 already passed → next is 2028-02-29 = 365 days
        assert rec.days_to_birthday(date(2027, 3, 1)) == 365


class TestRecordStr:
    def test_str_minimal(self) -> None:
        result = str(Record("Alice"))
        assert "Alice" in result
        assert "no phones" in result

    def test_str_with_phone(self) -> None:
        result = str(Record("Alice", phones=["0501234567"]))
        assert "0501234567" in result

    def test_str_with_email(self) -> None:
        result = str(Record("Alice", email="a@b.com"))
        assert "a@b.com" in result

    def test_str_with_birthday(self) -> None:
        result = str(Record("Alice", birthday="15.03.1990"))
        assert "15.03.1990" in result
