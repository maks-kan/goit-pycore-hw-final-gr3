import json
from models import AddressBook, Record
from decorators import input_error


def save_data(book, filename="addressbook.json"):
    """Зберігає AddressBook у JSON-файл."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(book.to_dict(), f, ensure_ascii=False, indent=4)


def load_data(filename="addressbook.json"):
    """
    Завантажує AddressBook із JSON-файлу.
    Якщо файл не знайдено або він пошкоджений — повертає нову AddressBook().
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return AddressBook.from_dict(data)
    except FileNotFoundError:
        return AddressBook()
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return AddressBook()


def show_help():
    """Показує список доступних команд."""
    commands = """
Available commands:

hello
    greet the bot

add <name> <phone>
    add new contact with phone
    
delete <name>
    delete contact

change-phone <name> <old_phone> <new_phone>
    change phone number

remove-phone <name> <phone>
    remove phone from contact

phone <name>
    show phones of contact

all
    show all contacts

add-birthday <name> <DD.MM.YYYY>
show-birthday <name>
change-birthday <name> <DD.MM.YYYY>
remove-birthday <name>

birthdays
    show upcoming birthdays

add-address <name> <address>
remove-address <name>
show-address <name>
change-address <name> <new_address>

add-email <name> <email>
remove-email <name>
show-email <name>
change-email <name> <new_email>

help
    show this help message

exit / close
    save contacts and exit program
"""
    return commands


@input_error
def add_contact(args, book: AddressBook):
    """Команда: add <name> <phone>"""
    name, phone, *_ = args

    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    record.add_phone(phone)
    return message


@input_error
def change_phone(args, book: AddressBook):
    """Команда: change <name> <old_phone> <new_phone>"""
    name, old_phone, new_phone = args

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.edit_phone(old_phone, new_phone)
    return "Phone updated."


@input_error
def remove_phone(args, book: AddressBook):
    """Команда: remove-phone <name> <phone>"""
    name, phone = args

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.remove_phone(phone)
    return "Phone removed."


@input_error
def delete_contact(args, book: AddressBook):
    """Команда: delete <name>"""
    name = args[0]
    book.delete(name)
    return "Contact deleted."


@input_error
def show_phone(args, book: AddressBook):
    """Команда: phone <name>"""
    name = args[0]

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    if not record.phones:
        return "No phone numbers for this contact."

    return "; ".join(p.value for p in record.phones)


@input_error
def show_all(args, book: AddressBook):
    """Команда: all"""
    if args:
        raise ValueError("Command 'all' does not take arguments.")

    if not book.data:
        return "No contacts saved."

    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    """Команда: add-birthday <name> <DD.MM.YYYY>"""
    name, birthday = args

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def change_birthday(args, book: AddressBook):
    """Команда: change-birthday <name> <DD.MM.YYYY>"""
    name, new_birthday = args

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.add_birthday(new_birthday)
    return "Birthday updated."


@input_error
def remove_birthday(args, book: AddressBook):
    """Команда: remove-birthday <name>"""
    name = args[0]

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.remove_birthday()
    return "Birthday removed."


@input_error
def show_birthday(args, book: AddressBook):
    """Команда: show-birthday <name>"""
    name = args[0]

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    if record.birthday is None:
        return "Birthday not set."

    return str(record.birthday)


@input_error
def add_address(args, book: AddressBook):
    """Команда: add-address <name> <address...>"""
    name = args[0]
    address = " ".join(args[1:])

    if not address:
        raise IndexError

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.add_address(address)
    return "Address added."


@input_error
def change_address(args, book: AddressBook):
    """Команда: change-address <name> <new_address...>"""
    name = args[0]
    new_address = " ".join(args[1:])

    if not new_address:
        raise IndexError

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.add_address(new_address)
    return "Address updated."


@input_error
def remove_address(args, book: AddressBook):
    """Команда: remove-address <name>"""
    name = args[0]

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.remove_address()
    return "Address removed."


@input_error
def show_address(args, book: AddressBook):
    """Команда: show-address <name>"""
    name = args[0]

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    if record.address is None:
        return "Address not set."

    return record.address.value


@input_error
def add_email(args, book: AddressBook):
    """Команда: add-email <name> <email>"""
    name, email = args

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.add_email(email)
    return "Email added."


@input_error
def change_email(args, book: AddressBook):
    """Команда: change-email <name> <new_email>"""
    name, new_email = args

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.add_email(new_email)
    return "Email updated."


@input_error
def remove_email(args, book: AddressBook):
    """Команда: remove-email <name>"""
    name = args[0]

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.remove_email()
    return "Email removed."


@input_error
def show_email(args, book: AddressBook):
    """Команда: show-email <name>"""
    name = args[0]

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    if record.email is None:
        return "Email not set."

    return record.email.value


@input_error
def birthdays(args, book: AddressBook):
    """Команда: birthdays"""
    if args:
        raise ValueError("Command 'birthdays' does not take arguments.")

    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No birthdays in the next 7 days."

    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in upcoming
    )