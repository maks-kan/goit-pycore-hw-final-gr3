from collections import defaultdict

from cli.colors import ColorScheme
from cli.commands import command
from cli.errors import AlreadyExistsError, NotFoundError, UsageError
from models.notebook import NoteBook


def _format_notes_table(notes: list, colors: ColorScheme) -> str:
    """Format a list of notes as an aligned table."""
    rows = []
    for note in notes:
        tags = ", ".join(note.tags) if note.tags else ""
        rows.append((note.title, note.text, tags))

    headers = ("Title", "Text", "Tags")
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def fmt(cells: tuple[str, ...]) -> str:
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)).rstrip()

    sep = f"{colors.TABLE_SEP}{'  '.join('─' * w for w in widths)}{colors.RESET}"
    header_line = f"{colors.HEADER}{fmt(headers)}{colors.RESET}"
    lines = [header_line, sep]
    lines.extend(fmt(row) for row in rows)
    return "\n".join(lines)


@command("Add a note. Usage: add-note <title> <text...>")
def handle_add_note(*args: str, notebook: NoteBook, colors: ColorScheme) -> str:
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
        raise AlreadyExistsError(f"Note '{title}' already exists.")
    return f"{colors.SUCCESS}Note '{title}' added.{colors.RESET}"


@command("Delete a note by title. Usage: delete-note <title>")
def handle_delete_note(*args: str, notebook: NoteBook, colors: ColorScheme) -> str:
    """
    Видаляє нотатку за назвою.

    Формат:
        delete-note <title>
    """
    if len(args) != 1:
        raise UsageError("title is required")

    title = args[0]

    if not notebook.delete_note(title):
        raise NotFoundError(f"Note '{title}' not found.")
    return f"{colors.SUCCESS}Note '{title}' deleted.{colors.RESET}"


@command("Edit note text. Usage: edit-note <title> <new_text...>")
def handle_edit_note(*args: str, notebook: NoteBook, colors: ColorScheme) -> str:
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
        raise NotFoundError(f"Note '{title}' not found.")
    return f"{colors.SUCCESS}Note '{title}' updated.{colors.RESET}"


@command("Rename a note. Usage: rename-note <title> <new_title>")
def handle_rename_note(*args: str, notebook: NoteBook, colors: ColorScheme) -> str:
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
        raise NotFoundError(f"Note '{title}' not found.")
    if not notebook.edit_note(title=title, new_title=new_title):
        raise AlreadyExistsError(
            f"Cannot rename note to '{new_title}'. It may already exist."
        )
    return f"{colors.SUCCESS}Note '{title}' renamed to '{new_title}'.{colors.RESET}"


@command("Add tags to a note. Usage: add-tags <title> <tag1> <tag2> ...")
def handle_add_tags(*args: str, notebook: NoteBook, colors: ColorScheme) -> str:
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
        raise NotFoundError(f"Note '{title}' not found.")
    note.add_tags(" ".join(tags))
    return f"{colors.SUCCESS}Tags added to note '{title}'.{colors.RESET}"


@command("Remove a tag from a note. Usage: remove-tag <title> <tag>")
def handle_remove_tag(*args: str, notebook: NoteBook, colors: ColorScheme) -> str:
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
        raise NotFoundError(f"Note '{title}' not found.")
    if not note.remove_tag(tag):
        raise NotFoundError(f"Tag '{tag}' not found in note '{title}'.")
    return f"{colors.SUCCESS}Tag '{tag}' removed from note '{title}'.{colors.RESET}"


@command("Search notes. Usage: search-notes <keyword>")
def handle_search_notes(*args: str, notebook: NoteBook, colors: ColorScheme) -> str:
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
        return f"{colors.SUCCESS}No notes found.{colors.RESET}"
    results.sort(key=lambda n: n.title.lower())
    return _format_notes_table(results, colors)


@command("Show all unique tags, sorted alphabetically.")
def handle_all_tags(*args: str, notebook: NoteBook, colors: ColorScheme) -> str:
    if args:
        raise UsageError("no arguments expected")

    tags = sorted({tag for note in notebook.notes for tag in note.tags})
    if not tags:
        return f"{colors.SUCCESS}No tags found.{colors.RESET}"
    return f"{colors.SUCCESS}{', '.join(tags)}{colors.RESET}"


@command("Show notes grouped by tag.")
def handle_notes_by_tag(*args: str, notebook: NoteBook, colors: ColorScheme) -> str:
    if args:
        raise UsageError("no arguments expected")

    if len(notebook) == 0:
        return f"{colors.SUCCESS}No notes saved.{colors.RESET}"

    tag_map: dict[str, list[tuple[str, str]]] = defaultdict(list)
    untagged: list[tuple[str, str]] = []
    for note in notebook.notes:
        entry = (note.title, note.text)
        if note.tags:
            for tag in note.tags:
                tag_map[tag].append(entry)
        else:
            untagged.append(entry)

    all_labels = list(tag_map) + (["untagged"] if untagged else [])
    # Total visible width: "── label ───…" — fixed for all tags.
    line_width = max(len(lbl) for lbl in all_labels) + 12 if all_labels else 0

    def _tag_header(label: str, colored_label: str) -> str:
        # "── " (3) + label + " " (1) + trailing "─"s
        trail = line_width - 3 - len(label) - 1
        sep = f"{colors.TABLE_SEP}{'─' * trail}{colors.RESET}"
        return f"── {colored_label} {sep}"

    def _note_line(title: str, text: str) -> str:
        return f"  {colors.DATA_BRIGHT}{title}{colors.RESET}: {text}"

    lines: list[str] = []
    for tag in sorted(tag_map):
        if lines:
            lines.append("")
        lines.append(_tag_header(tag, f"{colors.HEADER}{tag}{colors.RESET}"))
        for title, text in sorted(tag_map[tag], key=lambda e: e[0].lower()):
            lines.append(_note_line(title, text))

    if untagged:
        if lines:
            lines.append("")
        label_colored = f"{colors.TABLE_SEP}untagged{colors.RESET}"
        lines.append(_tag_header("untagged", label_colored))
        for title, text in sorted(untagged, key=lambda e: e[0].lower()):
            lines.append(_note_line(title, text))

    return "\n".join(lines)


@command("Show all notes.")
def handle_show_all_notes(*args: str, notebook: NoteBook, colors: ColorScheme) -> str:
    """
    Показує всі нотатки.
    """
    if args:
        raise UsageError("no arguments expected")

    if len(notebook) == 0:
        return f"{colors.SUCCESS}No notes saved.{colors.RESET}"
    notes = sorted(notebook.notes, key=lambda n: n.title.lower())
    return _format_notes_table(notes, colors)
