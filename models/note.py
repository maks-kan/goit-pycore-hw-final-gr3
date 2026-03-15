class Note:
    """Клас Note представляє одну нотатку з текстом і тегами."""

    def __init__(self, text: str, tags: list[str] = None):
        """
        Створює нову нотатку.
        :param text: Текст нотатки.
        :param tags: Список тегів (необов'язковий, за замовчуванням порожній).
        """
        self.text = text  # Зберігаємо текст нотатки
        self.tags = (
            tags if tags is not None else []
        )  # Зберігаємо список тегів (або порожній список)

    def matches(self, keyword: str) -> bool:
        """
        Перевіряє, чи містить нотатка задане ключове слово.
        Повертає True, якщо keyword є підрядком у тексті нотатки
        або входить в будь-який з тегів.
        """
        # Пошук ключового слова у тексті або серед тегів (без врахування регістру)
        keyword_lower = keyword.lower()
        text_lower = self.text.lower()
        if keyword_lower in text_lower:
            return True
        # Перевіряємо кожен тег (також у нижньому регістрі для коректного порівняння)
        for tag in self.tags:
            if keyword_lower in tag.lower():
                return True
        return False

    def __repr__(self) -> str:
        """Повертає рядкове представлення нотатки для зручного відображення."""
        return f"Note(text={self.text!r}, tags={self.tags!r})"
