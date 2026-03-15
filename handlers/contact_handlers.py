from cli.colors import ColorScheme
from cli.commands import command
from cli.errors import AlreadyExistsError, NotFoundError, UsageError
from models.address_book import AddressBook
from models.record import Record


def _format_phones(phones_str: str, colors: ColorScheme) -> str:
    """Highlight phone numbers in bright white, commas in default color."""
    if not phones_str:
        return ""
    parts = phones_str.split(", ")
    bright = [f"{colors.DATA_BRIGHT}{p}{colors.RESET}" for p in parts]
    return ", ".join(bright)


def _format_contacts_table(records: list[Record], colors: ColorScheme) -> str:
    """Format a list of records as an aligned table."""
    rows = []
    for r in records:
        phones = ", ".join(p.value for p in r.phones) if r.phones else ""
        email = r.email.value if r.email else ""
        bday = r.birthday.value.strftime("%d.%m.%Y") if r.birthday else ""
        rows.append((r.name.value, phones, email, bday))

    headers = ("Name", "Phones", "Email", "Birthday")
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def fmt(cells: tuple[str, ...]) -> str:
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)).rstrip()

    def fmt_row(row: tuple[str, ...]) -> str:
        """Format a data row with bright phones."""
        parts = []
        for i, cell in enumerate(row):
            padding = " " * (widths[i] - len(cell))
            if i == 1 and cell:  # Phones column
                parts.append(_format_phones(cell, colors) + padding)
            else:
                parts.append(cell + padding)
        return "  ".join(parts).rstrip()

    sep = f"{colors.TABLE_SEP}{'  '.join('─' * w for w in widths)}{colors.RESET}"
    header_line = f"{colors.HEADER}{fmt(headers)}{colors.RESET}"
    lines = [header_line, sep]
    lines.extend(fmt_row(row) for row in rows)
    return "\n".join(lines)


@command("Greet the bot.")
def handle_hello(*args: str, colors: ColorScheme) -> str:
    return f"{colors.SUCCESS}How can I help you?{colors.RESET}"


@command("Add a contact or phone. Usage: add <name> <phone>")
def handle_add_contact(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if len(args) < 2:
        raise UsageError("name and phone are required")
    name, phone = args[0], args[1]

    record = book.get_record(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        record.add_phone(phone)
        return f"{colors.SUCCESS}Contact added.{colors.RESET}"
    if not record.add_phone(phone):
        raise AlreadyExistsError("Phone already exists.")
    return f"{colors.SUCCESS}Contact updated.{colors.RESET}"


@command("Delete a contact. Usage: delete <name>")
def handle_delete_contact(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if not args:
        raise UsageError("name is required")
    if book.get_record(args[0]) is None:
        raise NotFoundError("Contact not found.")
    book.delete_record(args[0])
    return f"{colors.SUCCESS}Contact deleted.{colors.RESET}"


@command("Change a phone number. Usage: change-phone <name> <old> <new>")
def handle_change_phone(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if len(args) < 3:
        raise UsageError("name, old phone, and new phone are required")
    name, old_phone, new_phone = args[0], args[1], args[2]

    record = book.get_record(name)
    if record is None:
        raise NotFoundError("Contact not found.")
    record.edit_phone(old_phone, new_phone)
    return f"{colors.SUCCESS}Phone updated.{colors.RESET}"


@command("Remove a phone number. Usage: remove-phone <name> <phone>")
def handle_remove_phone(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if len(args) < 2:
        raise UsageError("name and phone are required")

    record = book.get_record(args[0])
    if record is None:
        raise NotFoundError("Contact not found.")
    record.remove_phone(args[1])
    return f"{colors.SUCCESS}Phone removed.{colors.RESET}"


@command("Show phones of a contact. Usage: phone <name>")
def handle_show_phone(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if not args:
        raise UsageError("name is required")

    record = book.get_record(args[0])
    if record is None:
        raise NotFoundError("Contact not found.")
    if not record.phones:
        return f"{colors.SUCCESS}No phone numbers for this contact.{colors.RESET}"
    return f"{colors.SUCCESS}{'; '.join(p.value for p in record.phones)}{colors.RESET}"


@command("Show all contacts.")
def handle_show_all(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if args:
        raise UsageError("no arguments expected")
    records = book.list_all()
    if not records:
        return f"{colors.SUCCESS}No contacts saved.{colors.RESET}"
    return _format_contacts_table(records, colors)


@command("Set birthday. Usage: add-birthday <name> <DD.MM.YYYY>")
def handle_add_birthday(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if len(args) < 2:
        raise UsageError("name and birthday are required")

    record = book.get_record(args[0])
    if record is None:
        raise NotFoundError("Contact not found.")
    record.edit_birthday(args[1])
    return f"{colors.SUCCESS}Birthday added.{colors.RESET}"


@command("Show birthday. Usage: show-birthday <name>")
def handle_show_birthday(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if not args:
        raise UsageError("name is required")

    record = book.get_record(args[0])
    if record is None:
        raise NotFoundError("Contact not found.")
    if record.birthday is None:
        raise NotFoundError("Birthday not set.")
    return f"{colors.SUCCESS}{record.birthday.value.strftime('%d.%m.%Y')}{colors.RESET}"


@command("Change birthday. Usage: change-birthday <name> <DD.MM.YYYY>")
def handle_change_birthday(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if len(args) < 2:
        raise UsageError("name and birthday are required")

    record = book.get_record(args[0])
    if record is None:
        raise NotFoundError("Contact not found.")
    record.edit_birthday(args[1])
    return f"{colors.SUCCESS}Birthday updated.{colors.RESET}"


@command("Remove birthday. Usage: remove-birthday <name>")
def handle_remove_birthday(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if not args:
        raise UsageError("name is required")

    record = book.get_record(args[0])
    if record is None:
        raise NotFoundError("Contact not found.")
    record.birthday = None
    return f"{colors.SUCCESS}Birthday removed.{colors.RESET}"


@command("Set email. Usage: add-email <name> <email>")
def handle_add_email(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if len(args) < 2:
        raise UsageError("name and email are required")

    record = book.get_record(args[0])
    if record is None:
        raise NotFoundError("Contact not found.")
    record.edit_email(args[1])
    return f"{colors.SUCCESS}Email added.{colors.RESET}"


@command("Show email. Usage: show-email <name>")
def handle_show_email(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if not args:
        raise UsageError("name is required")

    record = book.get_record(args[0])
    if record is None:
        raise NotFoundError("Contact not found.")
    if record.email is None:
        raise NotFoundError("Email not set.")
    return f"{colors.SUCCESS}{record.email.value}{colors.RESET}"


@command("Change email. Usage: change-email <name> <email>")
def handle_change_email(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if len(args) < 2:
        raise UsageError("name and email are required")

    record = book.get_record(args[0])
    if record is None:
        raise NotFoundError("Contact not found.")
    record.edit_email(args[1])
    return f"{colors.SUCCESS}Email updated.{colors.RESET}"


@command("Remove email. Usage: remove-email <name>")
def handle_remove_email(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if not args:
        raise UsageError("name is required")

    record = book.get_record(args[0])
    if record is None:
        raise NotFoundError("Contact not found.")
    record.email = None
    return f"{colors.SUCCESS}Email removed.{colors.RESET}"


@command("Search contacts. Usage: search <query>")
def handle_search(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if not args:
        raise UsageError("query is required")

    results = book.search(args[0])
    if not results:
        return f"{colors.SUCCESS}No contacts found.{colors.RESET}"
    return _format_contacts_table(results, colors)


@command("Show upcoming birthdays (next 7 days).")
def handle_birthdays(*args: str, book: AddressBook, colors: ColorScheme) -> str:
    if args:
        raise UsageError("no arguments expected")

    upcoming = []
    for record in book.list_all():
        days = record.days_to_birthday()
        if days is not None and days <= 7:
            bday = record.birthday.value.strftime("%d.%m.%Y")
            upcoming.append((record.name.value, days, bday))
    if not upcoming:
        return f"{colors.SUCCESS}No birthdays in the next 7 days.{colors.RESET}"
    upcoming.sort(key=lambda x: x[1])
    lines = [f"{name}: {bday} (in {days} day(s))" for name, days, bday in upcoming]
    return f"{colors.SUCCESS}{chr(10).join(lines)}{colors.RESET}"
