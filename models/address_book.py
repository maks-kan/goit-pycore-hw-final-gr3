from models.record import Record


class AddressBook:
    """Клас адресної книги для керування контактами."""

    def __init__(self) -> None:
        self.records: dict[str, Record] = {}  # Словник: ім'я -> Record

    def add_record(self, record: Record) -> None:
        """Додати запис (Record) до адресної книги."""
        name = record.name.value
        if name in self.records:
            # Якщо контакт з таким ім'ям вже існує, замінюємо його новим записом
            self.records[name] = record
        else:
            self.records[name] = record

    def get_record(self, name: str) -> Record | None:
        """Знайти контакт за повним ім'ям (точний збіг)."""
        return self.records.get(name)

    def delete_record(self, name: str) -> None:
        """Видалити контакт за ім'ям."""
        if name in self.records:
            del self.records[name]
        else:
            raise ValueError("Contact not found")

    def search(self, query: str) -> list[Record]:
        """Пошук контактів за підрядком (в імені, телефоні або email)."""
        results = []
        q = query.lower()
        for record in self.records.values():
            # Пошук незалежно від регістру
            if q in record.name.value.lower():
                results.append(record)
            elif any(q in p.value for p in record.phones):
                results.append(record)
            elif record.email and q in record.email.value.lower():
                results.append(record)
        return results

    def list_all(self) -> list[Record]:
        """Повернути список всіх контактів (об'єктів Record)."""
        return list(self.records.values())
