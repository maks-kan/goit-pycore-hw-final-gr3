import re


class Note:
    """Клас Note представляє одну нотатку з назвою, текстом і тегами."""

    TAG_PATTERN = re.compile(r"^[A-Za-zА-Яа-яЁёІіЇїЄє]+$")

    def __init__(self, title: str, text: str, tags: str | None = None):
        """
        Створює нову нотатку.

        :param title: Назва нотатки.
        :param text: Текст нотатки.
        :param tags: Рядок тегів через пробіл (необов'язковий).
        """
        self.title = title
        self.text = text
        self.tags: list[str] = []

        if tags:
            self.add_tags(tags)

    def add_tags(self, tags: str) -> None:
        """
        Додає один або кілька тегів до нотатки.

        Теги передаються рядком через пробіл:
        "work urgent idea"

        Кожен тег має містити лише літери.
        Дублікати не додаються.
        """
        for tag in tags.split():
            if not self.TAG_PATTERN.fullmatch(tag):
                raise ValueError(f"Invalid tag: {tag}")

            if tag not in self.tags:
                self.tags.append(tag)

    def remove_tag(self, tag: str) -> bool:
        """
        Видаляє тег із нотатки.

        Повертає True, якщо тег знайдено і видалено,
        і False, якщо такого тегу немає.
        """
        if tag in self.tags:
            self.tags.remove(tag)
            return True
        return False

    def matches(self, keyword: str) -> bool:
        """
        Перевіряє, чи містить нотатка задане ключове слово
        у назві, тексті або тегах.
        """
        keyword_lower = keyword.lower()

        if keyword_lower in self.title.lower():
            return True

        if keyword_lower in self.text.lower():
            return True

        for tag in self.tags:
            if keyword_lower in tag.lower():
                return True

        return False

    def __repr__(self) -> str:
        """Повертає зручне рядкове представлення нотатки."""
        tags_str = ", ".join(self.tags) if self.tags else "no tags"
        return f"Title: {self.title} | Text: {self.text} | Tags: {tags_str}"