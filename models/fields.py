from datetime import datetime


class Field:
    """Базовий клас поля, що зберігає значення."""

    def __init__(self, value):
        self.value = value  # Встановлення через setter (може містити валідацію)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # У базовому класі специфічна валідація не виконується
        self._value = value


class Name(Field):
    """Ім'я контакту."""

    @Field.value.setter
    def value(self, value):
        if not value:
            raise ValueError("Ім'я не може бути порожнім")
        self._value = value


class Phone(Field):
    """Телефонний номер, що складається з 10 цифр."""

    @Field.value.setter
    def value(self, value):
        if not value.isdigit():
            raise ValueError("Номер телефону має містити лише цифри")
        if len(value) != 10:
            raise ValueError("Номер телефону має містити рівно 10 цифр")
        self._value = value
        # Після успішної валідації зберігаємо номер


class Email(Field):
    """Email-адреса контакту."""

    @Field.value.setter
    def value(self, value):
        # Проста перевірка наявності '@' у рядку (не на початку чи в кінці)
        if value.count("@") != 1 or value.startswith("@") or value.endswith("@"):
            raise ValueError("Некоректна email-адреса")
        self._value = value


class Birthday(Field):
    """Дата народження контакту."""

    @Field.value.setter
    def value(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Дата народження має бути у форматі ДД.ММ.РРРР")
        # Зберігаємо лише дату (без часу)
        self._value = parsed_date.date()
