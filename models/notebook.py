from models.note import Note


class NoteBook:
    """Керує списком нотаток: додавання, пошук, редагування, видалення."""

    def __init__(self):
        """Ініціалізує записник порожнім списком нотаток."""
        self.notes: list[Note] = []

    def find_note_by_title(self, title: str) -> Note | None:
        """Повертає нотатку за назвою або None, якщо нотатку не знайдено."""
        for note in self.notes:
            if note.title == title:
                return note
        return None

    def add_note(self, title: str, text: str, tags: str | None = None) -> bool:
        """
        Додає нову нотатку з назвою, текстом і тегами.

        Повертає:
            True  - якщо нотатку успішно додано
            False - якщо нотатка з такою назвою вже існує
        """
        if self.find_note_by_title(title) is not None:
            return False

        new_note = Note(title, text, tags)
        self.notes.append(new_note)
        return True

    def delete_note(self, title: str) -> bool:
        """
        Видаляє нотатку за назвою.

        Повертає:
            True  - якщо нотатку успішно видалено
            False - якщо нотатку не знайдено
        """
        note = self.find_note_by_title(title)
        if note is None:
            return False

        self.notes.remove(note)
        return True

    def edit_note(
        self,
        title: str,
        new_title: str | None = None,
        new_text: str | None = None,
        new_tags: list[str] | None = None,
    ) -> bool:
        """
        Редагує існуючу нотатку за її назвою.

        Можна змінити:
        - назву
        - текст
        - теги

        Повертає:
            True  - якщо нотатку успішно оновлено
            False - якщо нотатку не знайдено або нова назва вже зайнята
        """
        note = self.find_note_by_title(title)
        if note is None:
            return False

        if new_title is not None and new_title != title:
            existing_note = self.find_note_by_title(new_title)
            if existing_note is not None:
                return False
            note.title = new_title

        if new_text is not None:
            note.text = new_text

        if new_tags is not None:
            note.tags = list(dict.fromkeys(new_tags))

        return True

    def search(self, keyword: str) -> list[Note]:
        """
        Шукає нотатки за ключовим словом у назві, тексті або тегах.
        Повертає список знайдених нотаток.
        """
        result = []

        for note in self.notes:
            if note.matches(keyword):
                result.append(note)

        return result

    def __len__(self) -> int:
        """Повертає кількість нотаток у записнику."""
        return len(self.notes)