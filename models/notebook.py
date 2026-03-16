from models.note import Note


class NoteBook:
    """Керує колекцією нотаток: додавання, пошук, редагування, видалення."""

    def __init__(self) -> None:
        """Ініціалізує записник порожнім словником нотаток."""
        self._notes: dict[str, Note] = {}

    @property
    def notes(self) -> list[Note]:
        """Повертає список усіх нотаток (для зворотної сумісності)."""
        return list(self._notes.values())

    def find_note_by_title(self, title: str) -> Note | None:
        """Повертає нотатку за назвою або None, якщо нотатку не знайдено."""
        return self._notes.get(title)

    def add_note(self, title: str, text: str, tags: str | None = None) -> bool:
        """
        Додає нову нотатку з назвою, текстом і тегами.

        Повертає:
            True  - якщо нотатку успішно додано
            False - якщо нотатка з такою назвою вже існує
        """
        if title in self._notes:
            return False

        self._notes[title] = Note(title, text, tags)
        return True

    def delete_note(self, title: str) -> bool:
        """
        Видаляє нотатку за назвою.

        Повертає:
            True  - якщо нотатку успішно видалено
            False - якщо нотатку не знайдено
        """
        if title not in self._notes:
            return False

        del self._notes[title]
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
        note = self._notes.get(title)
        if note is None:
            return False

        if new_title is not None and new_title != title:
            if new_title in self._notes:
                return False
            del self._notes[title]
            note.title = new_title
            self._notes[new_title] = note

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
        return [note for note in self._notes.values() if note.matches(keyword)]

    def __len__(self) -> int:
        """Повертає кількість нотаток у записнику."""
        return len(self._notes)
