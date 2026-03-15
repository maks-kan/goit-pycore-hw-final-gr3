from models.note import Note


class NoteBook:
    """Керує списком нотаток (додавання, пошук, редагування, видалення)."""

    def __init__(self):
        """Ініціалізує записник порожнім списком нотаток."""
        self.notes: list[Note] = []  # список з об'єктів Note

    def add_note(self, text: str, tags: list[str] = None) -> None:
        """Додає нову нотатку з заданим текстом та тегами до записника."""
        new_note = Note(text, tags)  # створюємо об'єкт Note
        self.notes.append(new_note)  # додаємо його до списку нотаток

    def delete_note(self, index: int) -> bool:
        """Видаляє нотатку за індексом у списку.

        Повертає True якщо успішно, False якщо індекс некоректний.
        """
        if 0 <= index < len(self.notes):
            self.notes.pop(index)  # видаляємо нотатку зі списку
            return True
        return False  # якщо індекс не валідний

    def edit_note(
        self, index: int, new_text: str = None, new_tags: list[str] = None
    ) -> bool:
        """
        Редагує існуючу нотатку за заданим індексом.
        Можна змінити текст, теги або і те, і інше (якщо передано).
        Повертає True у разі успіху або False, якщо індекс некоректний.
        """
        if 0 <= index < len(self.notes):
            note = self.notes[index]
            if new_text is not None:
                note.text = new_text  # оновлюємо текст нотатки
            if new_tags is not None:
                note.tags = new_tags  # оновлюємо список тегів
            return True
        return False

    def search(self, keyword: str) -> list[Note]:
        """
        Шукає нотатки, що містять задане ключове слово у тексті або тегах.
        Повертає список знайдених нотаток (може бути порожнім, якщо нічого не знайдено).
        """
        result = []
        for note in self.notes:
            if note.matches(keyword):
                result.append(note)
        return result

    def __len__(self) -> int:
        """Повертає кількість нотаток у записнику."""
        return len(self.notes)
