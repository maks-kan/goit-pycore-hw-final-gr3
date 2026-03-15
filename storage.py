import json
from pathlib import Path

from models.address_book import AddressBook
from models.notebook import NoteBook
from models.record import Record

CONTACTS_FILE = Path("contacts.json")
NOTES_FILE = Path("notes.json")


def save_contacts(book: AddressBook) -> None:
    """Serialize all contacts to JSON."""
    data = []
    for record in book.list_all():
        entry: dict = {
            "name": record.name.value,
            "phones": [p.value for p in record.phones],
        }
        if record.email:
            entry["email"] = record.email.value
        if record.birthday:
            entry["birthday"] = record.birthday.value.strftime("%d.%m.%Y")
        data.append(entry)
    CONTACTS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8"
    )


def load_contacts() -> AddressBook:
    """Load contacts from JSON. Returns empty book if file is missing."""
    book = AddressBook()
    try:
        data = json.loads(CONTACTS_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError, json.JSONDecodeError:
        return book
    for entry in data:
        record = Record(
            name=entry["name"],
            phones=entry.get("phones"),
            email=entry.get("email"),
            birthday=entry.get("birthday"),
        )
        book.add_record(record)
    return book


def save_notes(notebook: NoteBook) -> None:
    """Serialize all notes to JSON."""
    data = [{"text": note.text, "tags": note.tags} for note in notebook.notes]
    NOTES_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8"
    )


def load_notes() -> NoteBook:
    """Load notes from JSON. Returns empty notebook if file is missing."""
    notebook = NoteBook()
    try:
        data = json.loads(NOTES_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError, json.JSONDecodeError:
        return notebook
    for item in data:
        notebook.add_note(item.get("text", ""), item.get("tags", []))
    return notebook
