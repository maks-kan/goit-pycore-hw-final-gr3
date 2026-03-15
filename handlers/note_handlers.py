from decorators import input_error


try:
    from note_models import NoteBook, Note
except ImportError:
    class Note:
        """Заглушка для класу Note."""

        def __init__(self, title, content=""):
            self.title = title
            self.content = content
            self.tags = []
            self.created_at = None
            self.updated_at = None

        def update_title(self, new_title):
            self.title = new_title

        def update_content(self, new_content):
            self.content = new_content

        def remove_content(self):
            self.content = ""

        def add_tag(self, tag):
            self.tags.append(tag)

        def remove_tag(self, tag):
            self.tags.remove(tag)

        def __str__(self):
            return (
                f"Title: {self.title}, "
                f"Content: {self.content}, "
                f"Tags: {', '.join(self.tags)}, "
                f"Created: {self.created_at}, "
                f"Updated: {self.updated_at}"
            )

    class NoteBook:
        """Заглушка для класу NoteBook."""

        def __init__(self):
            self.data = {}

        def add_note(self, note):
            self.data[note.title] = note

        def find_by_title(self, title):
            return self.data.get(title)

        def delete(self, title):
            if title not in self.data:
                raise KeyError("Note not found.")
            del self.data[title]

        def find_by_tag(self, tag):
            return [
                note for note in self.data.values()
                if tag in note.tags
            ]


def parse_note_input(user_input: str):
    """Розбирає введений рядок на команду та аргументи."""
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def show_note_help():
    """Показує список доступних команд для роботи із нотатками."""
    commands = """
Available note commands:

add-note <title> <content>
    add new note

change-note-title <old_title> <new_title>
    change note title

change-note-content <title> <new_content>
    change note content

remove-note-content <title>
    remove note content

delete-note <title>
    delete note by title

add-tag <title> <tag>
    add tag to note

remove-tag <title> <tag>
    remove tag from note

find-note-by-title <title>
    find note by title

find-notes-by-tag <tag>
    find notes by tag

all-notes
    show all notes
"""
    return commands


@input_error
def add_note(args, notebook: NoteBook):
    """Команда: add-note <title> <content...>"""
    title = args[0]
    content = " ".join(args[1:])

    if not title:
        raise IndexError

    note = notebook.find_by_title(title)
    if note is not None:
        raise ValueError("Note with this title already exists.")

    new_note = Note(title, content)
    notebook.add_note(new_note)
    return "Note added."


@input_error
def change_note_title(args, notebook: NoteBook):
    """Команда: change-note-title <old_title> <new_title>"""
    old_title, new_title = args

    note = notebook.find_by_title(old_title)
    if note is None:
        raise KeyError("Note not found.")

    if notebook.find_by_title(new_title) is not None:
        raise ValueError("Note with this new title already exists.")

    notebook.delete(old_title)
    note.update_title(new_title)
    notebook.add_note(note)

    return "Note title updated."


@input_error
def change_note_content(args, notebook: NoteBook):
    """Команда: change-note-content <title> <new_content...>"""
    title = args[0]
    new_content = " ".join(args[1:])

    if not new_content:
        raise IndexError

    note = notebook.find_by_title(title)
    if note is None:
        raise KeyError("Note not found.")

    note.update_content(new_content)
    return "Note content updated."


@input_error
def remove_note_content(args, notebook: NoteBook):
    """Команда: remove-note-content <title>"""
    title = args[0]

    note = notebook.find_by_title(title)
    if note is None:
        raise KeyError("Note not found.")

    note.remove_content()
    return "Note content removed."


@input_error
def delete_note(args, notebook: NoteBook):
    """Команда: delete-note <title>"""
    title = args[0]
    notebook.delete(title)
    return "Note deleted."


@input_error
def add_tag(args, notebook: NoteBook):
    """Команда: add-tag <title> <tag>"""
    title, tag = args

    note = notebook.find_by_title(title)
    if note is None:
        raise KeyError("Note not found.")

    note.add_tag(tag)
    return "Tag added."


@input_error
def remove_tag(args, notebook: NoteBook):
    """Команда: remove-tag <title> <tag>"""
    title, tag = args

    note = notebook.find_by_title(title)
    if note is None:
        raise KeyError("Note not found.")

    note.remove_tag(tag)
    return "Tag removed."


@input_error
def find_note_by_title(args, notebook: NoteBook):
    """Команда: find-note-by-title <title>"""
    title = args[0]

    note = notebook.find_by_title(title)
    if note is None:
        raise KeyError("Note not found.")

    return str(note)


@input_error
def find_notes_by_tag(args, notebook: NoteBook):
    """Команда: find-notes-by-tag <tag>"""
    tag = args[0]

    notes = notebook.find_by_tag(tag)
    if not notes:
        return "No notes found with this tag."

    return "\n".join(str(note) for note in notes)


@input_error
def show_all_notes(args, notebook: NoteBook):
    """Команда: all-notes"""
    if args:
        raise ValueError("Command 'all-notes' does not take arguments.")

    if not notebook.data:
        return "No notes saved."

    return "\n".join(str(note) for note in notebook.data.values())