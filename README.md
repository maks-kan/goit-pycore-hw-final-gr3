# Персональний помічник — Фінальний груповий проєкт

## Команда

- Olga Shadrunova
- Maks Kaniuka
- Ivan Bochkarov
- Oleksandr Semychenkov

## Мета проєкту

Створити консольну систему "Персональний помічник" для зберігання контактів та нотаток. Дані зберігаються на диску і не втрачаються при перезапуску програми.

---

## Основні вимоги

### Контакти

- Додавання контактів (ім'я, адреса, телефон, email, день народження)
- Пошук контактів (наприклад, за іменем)
- Редагування та видалення контактів
- Показ контактів, у яких день народження через N днів
- Валідація телефону та email при додаванні/редагуванні

### Нотатки

- Додавання текстових нотаток
- Пошук, редагування та видалення нотаток

### Збереження даних

- Дані зберігаються у файлі на диску (JSON)
- Перезапуск програми не видаляє дані

---

## Розподіл завдань

### Розробник 1 — Моделі даних та збереження

Створює класи, з якими працюватимуть усі інші. Починає першим.

| # | Завдання | Файл |
|---|----------|------|
| 1 | Клас `Field` (базовий) та похідні: `Name`, `Phone`, `Email`, `Birthday` | `models/fields.py` |
| 2 | Валідація `Phone` та `Email` | `models/fields.py` |
| 3 | Клас `Record` — один контакт з усіма полями | `models/record.py` |
| 4 | Клас `AddressBook` — колекція контактів (`add_record`, `find`, `delete`, `search`) | `models/address_book.py` |
| 5 | Клас `Note` та `NoteBook` — колекція нотаток з підтримкою тегів | `models/note.py`, `models/notebook.py` |
| 6 | Збереження/завантаження даних на диск (JSON) | `storage.py` |

### Розробник 2 — Обробники команд (handlers)

Пише функції, які виконують команди користувача. Підключається, коли моделі від Розробника 1 готові.

| # | Завдання | Файл |
|---|----------|------|
| 1 | `handle_add_contact` — додавання контакту | `handlers/contact_handlers.py` |
| 2 | `handle_change_phone`, `handle_remove_phone` — зміна/видалення телефону | `handlers/contact_handlers.py` |
| 3 | `handle_delete_contact` — видалення контакту | `handlers/contact_handlers.py` |
| 4 | `handle_search` — пошук контактів за іменем, телефоном або email | `handlers/contact_handlers.py` |
| 5 | `handle_show_all` — показ усіх контактів | `handlers/contact_handlers.py` |
| 6 | `handle_birthdays` — дні народження протягом 7 днів | `handlers/contact_handlers.py` |
| 7 | Обробники email та birthday (add/show/change/remove) | `handlers/contact_handlers.py` |
| 8 | `handle_add_note`, `handle_edit_note`, `handle_delete_note`, `handle_search_notes`, `handle_show_all_notes` | `handlers/note_handlers.py` |

### Розробник 3 — CLI-інтерфейс (головна програма)

Створює основний файл програми та все, що бачить користувач. Може працювати паралельно з Розробником 1 (використовуючи заглушки).

| # | Завдання | Файл |
|---|----------|------|
| 1 | Головний цикл програми: REPL, парсинг вводу, підказки команд | `cli/repl.py` |
| 2 | Реєстрація та маршрутизація команд | `cli/commands.py` |
| 3 | Кольорова схема виводу, підтримка `--no-color` | `cli/colors.py` |
| 4 | Клас `UsageError` для помилок введення | `cli/errors.py` |
| 5 | Точка входу, завантаження/збереження даних, bootstrap команд | `main.py` |

---

## Порядок роботи

1. **Розробник 1** починає першим — створює моделі. Поки моделі не готові, інші можуть працювати з заглушками.
2. **Розробник 3** починає паралельно — створює скелет `main.py` з заглушками команд.
3. **Розробник 2** підключається, коли класи `Record`, `AddressBook`, `Note`, `NoteBook` готові — пише обробники.
4. Наприкінці — усі інтегрують код разом через `main` гілку.

---

## Структура проєкту

```
goit-pycore-hw-final-gr3/
├── main.py                  # Точка входу
├── storage.py               # Збереження даних (JSON)
├── pyproject.toml           # Залежності та налаштування проєкту
├── uv.lock                  # Lock-файл залежностей
├── models/
│   ├── __init__.py
│   ├── fields.py            # Поля та валідація
│   ├── record.py            # Клас Record
│   ├── address_book.py      # Клас AddressBook
│   ├── note.py              # Клас Note
│   └── notebook.py          # Клас NoteBook
├── handlers/
│   ├── __init__.py
│   ├── contact_handlers.py  # Обробники контактів
│   └── note_handlers.py     # Обробники нотаток
├── cli/
│   ├── __init__.py
│   ├── colors.py            # Кольорова схема виводу
│   ├── commands.py          # Реєстрація команд
│   ├── errors.py            # Обробка помилок (UsageError)
│   └── repl.py              # Головний REPL-цикл та парсинг вводу
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_address_book.py
│   ├── test_colors.py
│   ├── test_commands.py
│   ├── test_contact_handlers.py
│   ├── test_fields.py
│   ├── test_main.py
│   ├── test_note_handlers.py
│   ├── test_notebook.py
│   ├── test_record.py
│   └── test_storage.py
├── .github/
│   └── workflows/
│       └── ci.yml           # CI-пайплайн
└── README.md
```

---

## Початок роботи

### 1. Клонування та налаштування

```bash
git clone https://github.com/maks-kan/goit-pycore-hw-final-gr3.git
cd goit-pycore-hw-final-gr3
```

### 2. Встановлення залежностей

Проєкт використовує [uv](https://docs.astral.sh/uv/getting-started/installation/) для керування залежностями.

```bash
uv sync
```

### 3. Увімкнення git-хуків

Хуки автоматично перевіряють форматування та лінтинг перед кожним комітом, а тести — перед кожним push.

```bash
git config core.hooksPath .githooks
```

### 4. Запуск програми

```bash
uv run python main.py

# Запуск з демо-даними (без завантаження з диску)
uv run python main.py --demo

# Вимкнення кольорового виводу
uv run python main.py --no-color
```

### 5. Запуск тестів та перевірок

```bash
# Запуск тестів
uv run pytest

# Перевірка форматування
uv run ruff format --check .

# Перевірка лінтером
uv run ruff check .

# Автоматичне форматування (виправляє файли)
uv run ruff format .
```

---

## Як працювати з Git (покрокова інструкція)

### 1. Створення своєї гілки

Кожен розробник працює у своїй гілці. **Ніколи не пишіть код прямо в `main`!**

```bash
git checkout -b dev-ваше-імʼя
```

Наприклад:
```bash
git checkout -b dev-olga
git checkout -b dev-ivan
git checkout -b dev-oleksandr
```

### 2. Щоденна робота: збереження змін

Після того як ви написали/змінили код:

```bash
# 1. Перевірте, що змінилось
git status

# 2. Додайте файли до комміту
git add назва_файлу.py
# Або додати всі змінені файли:
git add .

# 3. Створіть комміт з описом що зробили
git commit -m "Додано клас Record з валідацією телефону"

# 4. Відправте зміни на GitHub
git push origin dev-ваше-імʼя
```

### 3. Створення Pull Request (злиття коду в main)

Коли ваша частина роботи готова:

1. Переконайтесь, що всі зміни запушені (`git push origin dev-ваше-імʼя`)
2. Відкрийте репозиторій у браузері: https://github.com/maks-kan/goit-pycore-hw-final-gr3
3. Натисніть кнопку **"Compare & pull request"** (з'явиться після push)
4. Або перейдіть у вкладку **Pull requests** → **New pull request**
5. Виберіть: `base: main` ← `compare: dev-ваше-імʼя`
6. Напишіть опис того, що було зроблено
7. Натисніть **"Create pull request"**
8. Зачекайте на ревью від тімліда (Maks) перед злиттям

### 4. Оновлення своєї гілки з main

Якщо хтось інший вже злив свій код у `main`, підтягніть ці зміни до себе:

```bash
# Перейдіть на main і підтягніть зміни
git checkout main
git pull origin main

# Поверніться у свою гілку і влийте зміни з main
git checkout dev-ваше-імʼя
git merge main
```

Якщо виникнуть конфлікти — вирішіть їх у файлах (між `<<<<<<<` та `>>>>>>>`) і зробіть новий комміт.

### Схема гілок

```
main ─────────────────────────────── (фінальний код)
  │
  ├── dev-olga ──────── (моделі)
  │
  ├── dev-ivan ──────── (обробники)
  │
  └── dev-oleksandr ─── (CLI)
```

---

## Команди помічника (help)

### Загальні

| Команда | Опис |
|---|---|
| `hello` | Привітання |
| `help` | Показати довідку |
| `quit` / `exit` / `close` | Вийти з програми |

### Контакти

| Команда | Опис |
|---|---|
| `add <name> <phone>` | Додати контакт або телефон |
| `delete <name>` | Видалити контакт |
| `all` | Показати всі контакти (відсортовано за іменем) |
| `search <query>` | Пошук контактів за іменем, телефоном або email |
| `phone <name>` | Показати телефони контакту |
| `change-phone <name> <old> <new>` | Змінити номер телефону |
| `delete-phone <name> <phone>` | Видалити номер телефону |
| `add-birthday <name> <DD.MM.YYYY>` | Додати день народження |
| `show-birthday <name>` | Показати день народження |
| `change-birthday <name> <DD.MM.YYYY>` | Змінити день народження |
| `delete-birthday <name>` | Видалити день народження |
| `birthdays` | Дні народження протягом 7 днів |
| `add-email <name> <email>` | Додати email |
| `show-email <name>` | Показати email |
| `change-email <name> <email>` | Змінити email |
| `delete-email <name>` | Видалити email |

### Нотатки

| Команда | Опис |
|---|---|
| `add-note <title> <text...>` | Додати нотатку |
| `edit-note <title> <new_text...>` | Редагувати текст нотатки |
| `rename-note <title> <new_title>` | Перейменувати нотатку |
| `delete-note <title>` | Видалити нотатку |
| `search-notes <keyword>` | Пошук нотаток за назвою, текстом або тегами |
| `all-notes` | Показати всі нотатки (відсортовано за назвою) |
| `add-tags <title> <tag1> <tag2> ...` | Додати теги до нотатки |
| `delete-tag <title> <tag>` | Видалити тег з нотатки |
| `all-tags` | Показати всі унікальні теги (відсортовано) |
| `notes-by-tag` | Показати нотатки згруповані за тегами |

---

## Бонусні завдання

### Бонус 1: Теги для нотаток — реалізовано

Повна підтримка тегів: додавання (`add-tags`), видалення (`delete-tag`), перегляд усіх тегів (`all-tags`), групування нотаток за тегами (`notes-by-tag`), пошук за тегами (`search-notes`).

### Бонус 2: Інтелектуальний аналіз команд — реалізовано

Якщо користувач ввів нерозпізнану команду, програма пропонує найближчу за допомогою `difflib.get_close_matches` (cutoff 0.6).

- **Реалізація:** `cli/repl.py`

---
