from datetime import date, datetime


class Field:
    """Базовий клас поля, що зберігає значення."""

    def __init__(self, value: str) -> None:
        self.value = value  # Встановлення через setter (може містити валідацію)

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        # У базовому класі специфічна валідація не виконується
        self._value = value


class Name(Field):
    """Ім'я контакту."""

    @Field.value.setter
    def value(self, value: str) -> None:
        if not value:
            raise ValueError("Name cannot be empty")
        self._value = value


class Phone(Field):
    """Телефонний номер, що складається з 10 цифр."""

    @Field.value.setter
    def value(self, value: str) -> None:
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        self._value = value


class Email(Field):
    """Email-адреса контакту."""

    @Field.value.setter
    def value(self, value: str) -> None:
        # Проста перевірка наявності '@' у рядку (не на початку чи в кінці)
        if value.count("@") != 1 or value.startswith("@") or value.endswith("@"):
            raise ValueError("Invalid email address")
        self._value = value


class Birthday(Field):
    """Дата народження контакту."""

    @property
    def value(self) -> date:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Birthday must be in DD.MM.YYYY format")
        # Зберігаємо лише дату (без часу)
        self._value = parsed_date.date()
