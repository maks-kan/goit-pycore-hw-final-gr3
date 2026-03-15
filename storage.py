import json

from models.notebook import NoteBook

CONTACTS_FILE = "contacts.json"
NOTES_FILE = "notes.json"

# ... (існуючі функції для контактів, напр. save_contacts, load_contacts)


def save_notes(note_book: "NoteBook") -> None:
    """
    Зберігає всі нотатки з NoteBook в файл notes.json (у форматі JSON).
    """
    notes_data = []
    # Формуємо список словників з даними нотаток
    for note in note_book.notes:
        notes_data.append({"text": note.text, "tags": note.tags})
    # Записуємо список у файл JSON
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes_data, f, ensure_ascii=False, indent=4)
    # Файл тепер містить JSON-масив нотаток з усіма текстами і тегами


def load_notes() -> "NoteBook":
    """
    Завантажує нотатки з файлу notes.json і повертає об'єкт NoteBook.
    Якщо файл відсутній або порожній, повертає порожній NoteBook.
    """
    note_book = NoteBook()
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes_data = json.load(f)  # читаємо список словників з файлу
    except FileNotFoundError:
        notes_data = []
    # Відновлюємо нотатки на основі прочитаних даних
    for item in notes_data:
        text = item.get("text", "")
        tags = item.get("tags", [])
        note_book.add_note(text, tags)
    return note_book
