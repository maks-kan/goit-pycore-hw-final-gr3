from cli.commands import command
from cli.errors import UsageError
from models.notebook import NoteBook


@command("Add a note. Usage: add-note <text...>")
def handle_add_note(*args: str, notebook: NoteBook) -> str:
    if not args:
        raise UsageError("text is required")
    text = " ".join(args)
    notebook.add_note(text)
    return "Note added."


@command("Delete a note by number. Usage: delete-note <number>")
def handle_delete_note(*args: str, notebook: NoteBook) -> str:
    if not args:
        raise UsageError("number is required")
    try:
        index = int(args[0]) - 1
    except ValueError:
        raise UsageError("number must be an integer")
    if not notebook.delete_note(index):
        return "Note not found (invalid number)."
    return "Note deleted."


@command("Edit note text. Usage: edit-note <number> <text...>")
def handle_edit_note(*args: str, notebook: NoteBook) -> str:
    if len(args) < 2:
        raise UsageError("number and new text are required")
    try:
        index = int(args[0]) - 1
    except ValueError:
        raise UsageError("number must be an integer")
    new_text = " ".join(args[1:])
    if not notebook.edit_note(index, new_text=new_text):
        return "Note not found (invalid number)."
    return "Note updated."


@command("Search notes. Usage: search-notes <keyword>")
def handle_search_notes(*args: str, notebook: NoteBook) -> str:
    if not args:
        raise UsageError("keyword is required")

    results = notebook.search(args[0])
    if not results:
        return "No notes found."
    lines = [f"  {i}. {note!r}" for i, note in enumerate(results, 1)]
    return "\n".join(lines)


@command("Show all notes.")
def handle_show_all_notes(*args: str, notebook: NoteBook) -> str:
    if args:
        raise UsageError("no arguments expected")
    if len(notebook) == 0:
        return "No notes saved."
    lines = [f"  {i}. {note!r}" for i, note in enumerate(notebook.notes, 1)]
    return "\n".join(lines)
