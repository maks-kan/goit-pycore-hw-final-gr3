from cli.commands import command
from cli.errors import UsageError
from models.notebook import NoteBook


def _format_note(note) -> str:
    """Форматує одну нотатку для зручного відображення."""
    return repr(note)


@command("Add a note. Usage: add-note <title> <text...>")
def handle_add_note(*args: str, notebook: NoteBook) -> str:
    """
    Додає нову нотатку.

    Формат:
        add-note <title> <text...>
    """
    if len(args) < 2:
        raise UsageError("title and text are required")

    title = args[0]
    text = " ".join(args[1:])

    if not notebook.add_note(title=title, text=text):
        return f"Note '{title}' already exists."

    return f"Note '{title}' added."


@command("Delete a note by title. Usage: delete-note <title>")
def handle_delete_note(*args: str, notebook: NoteBook) -> str:
    """
    Видаляє нотатку за назвою.

    Формат:
        delete-note <title>
    """
    if len(args) != 1:
        raise UsageError("title is required")

    title = args[0]

    if not notebook.delete_note(title):
        return f"Note '{title}' not found."

    return f"Note '{title}' deleted."


@command("Edit note text. Usage: edit-note <title> <new_text...>")
def handle_edit_note(*args: str, notebook: NoteBook) -> str:
    """
    Редагує текст нотатки за її назвою.

    Формат:
        edit-note <title> <new_text...>
    """
    if len(args) < 2:
        raise UsageError("title and new text are required")

    title = args[0]
    new_text = " ".join(args[1:])

    if not notebook.edit_note(title=title, new_text=new_text):
        return f"Note '{title}' not found."

    return f"Note '{title}' updated."


@command("Rename a note. Usage: rename-note <title> <new_title>")
def handle_rename_note(*args: str, notebook: NoteBook) -> str:
    """
    Змінює назву нотатки.

    Формат:
        rename-note <title> <new_title>
    """
    if len(args) != 2:
        raise UsageError("title and new title are required")

    title = args[0]
    new_title = args[1]

    note = notebook.find_note_by_title(title)
    if note is None:
        return f"Note '{title}' not found."

    if not notebook.edit_note(title=title, new_title=new_title):
        return f"Cannot rename note to '{new_title}'. It may already exist."

    return f"Note '{title}' renamed to '{new_title}'."


@command("Add tags to a note. Usage: add-tags <title> <tag1> <tag2> ...")
def handle_add_tags(*args: str, notebook: NoteBook) -> str:
    """
    Додає один або кілька тегів до нотатки.

    Формат:
        add-tags <title> <tag1> <tag2> ...
    """
    if len(args) < 2:
        raise UsageError("title and at least one tag are required")

    title = args[0]
    tags = args[1:]

    note = notebook.find_note_by_title(title)
    if note is None:
        return f"Note '{title}' not found."

    try:
        note.add_tags(" ".join(tags))
    except ValueError as error:
        return str(error)

    return f"Tags added to note '{title}'."


@command("Remove a tag from a note. Usage: remove-tag <title> <tag>")
def handle_remove_tag(*args: str, notebook: NoteBook) -> str:
    """
    Видаляє один тег із нотатки.

    Формат:
        remove-tag <title> <tag>
    """
    if len(args) != 2:
        raise UsageError("title and tag are required")

    title = args[0]
    tag = args[1]

    note = notebook.find_note_by_title(title)
    if note is None:
        return f"Note '{title}' not found."

    if not note.remove_tag(tag):
        return f"Tag '{tag}' not found in note '{title}'."

    return f"Tag '{tag}' removed from note '{title}'."


@command("Search notes. Usage: search-notes <keyword>")
def handle_search_notes(*args: str, notebook: NoteBook) -> str:
    """
    Шукає нотатки за ключовим словом у назві, тексті або тегах.

    Формат:
        search-notes <keyword>
    """
    if len(args) != 1:
        raise UsageError("keyword is required")

    keyword = args[0]
    results = notebook.search(keyword)

    if not results:
        return "No notes found."

    lines = [f"  {i}. {_format_note(note)}" for i, note in enumerate(results, 1)]
    return "\n".join(lines)


@command("Show all notes.")
def handle_show_all_notes(*args: str, notebook: NoteBook) -> str:
    """
    Показує всі нотатки.
    """
    if args:
        raise UsageError("no arguments expected")

    if len(notebook) == 0:
        return "No notes saved."

    lines = [f"  {i}. {_format_note(note)}" for i, note in enumerate(notebook.notes, 1)]
    return "\n".join(lines)