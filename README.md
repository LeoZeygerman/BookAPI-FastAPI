# 📚 Book API

REST API для управления книгами и авторами на **FastAPI + PostgreSQL + SQLAlchemy**.

Учебный проект для практики backend-разработки на Python, работы с PostgreSQL, SQLAlchemy ORM, CRUD-операциями и связями между таблицами.

---

## 🚀 Возможности

### 📖 Работа с книгами

- Создание книги
- Получение списка всех книг
- Получение книги по ID
- Обновление книги
- Удаление книги
- Поиск книг по автору

### 👤 Работа с авторами

- Поиск автора
- Получение автора вместе со всеми его книгами
- Удаление автора вместе со всеми его книгами

### 🔗 Связи между таблицами

В проекте реализована связь:

```text
Author 1 ──────── N Book
```

Один автор может иметь несколько книг, при этом каждая книга принадлежит одному автору.

Для связи используются:

- `ForeignKey`
- `relationship`
- `back_populates`

---

## 🛠 Технологии

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- asyncpg
- Uvicorn

---

## 📁 Структура проекта

```text
BookAPI/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   └── router/
│       ├── books.py
│       └── authors.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### Основные файлы

**`main.py`** — создание FastAPI-приложения и подключение роутеров.

**`database.py`** — настройка подключения к PostgreSQL и создание асинхронной сессии SQLAlchemy.

**`models.py`** — ORM-модели базы данных и связи между ними.

**`schemas.py`** — Pydantic-модели для валидации входных данных и формирования ответов API.

**`router/`** — API-маршруты для работы с книгами и авторами.

---

## 🗄 Структура базы данных

### Таблица `authors`

| Поле | Тип | Описание |
|---|---|---|
| `id` | Integer | Уникальный идентификатор автора |
| `name` | String | Имя автора |

### Таблица `books`

| Поле | Тип | Описание |
|---|---|---|
| `id` | Integer | Уникальный идентификатор книги |
| `title` | String | Название книги |
| `note` | String | Описание / заметка |
| `author_id` | Integer | ID автора |

Связь между таблицами:

```text
authors.id
    ↑
    │
books.author_id
```

Физически связь в базе данных хранится через `books.author_id`, который является внешним ключом на `authors.id`.

---

# 📡 API

## 📖 Книги

### Получить все книги

```http
GET /books/
```

Возвращает список всех книг.

---

### Получить книгу по ID

```http
GET /books/{book_id}
```

Пример:

```http
GET /books/1
```

Пример ответа:

```json
{
    "id": 1,
    "title": "The Hobbit",
    "note": "Fantasy",
    "author": "J. R. R. Tolkien"
}
```

---

### Создать книгу

```http
POST /books/
```

Пример запроса:

```json
{
    "title": "The Hobbit",
    "note": "Fantasy",
    "author": {
        "name": "J. R. R. Tolkien"
    }
}
```

При создании книги API:

1. Ищет автора по имени.
2. Если автор уже существует — использует существующую запись.
3. Если автора нет — создаёт нового.
4. Создаёт книгу.
5. Связывает книгу с автором через SQLAlchemy `relationship`.

Таким образом, клиенту не нужно передавать `author_id`.

---

### Обновить книгу

```http
PATCH /books/{book_id}
```

Пример запроса:

```json
{
    "title": "The Hobbit: There and Back Again",
    "note": "Updated description"
}
```

---

### Удалить книгу

```http
DELETE /books/{book_id}
```

Удаляет указанную книгу.

---

### Найти книги по автору

```http
GET /books/author/{author_name}
```

Пример:

```http
GET /books/author/Tolkien
```

Возвращает книги указанного автора.

---

# 👤 Авторы

### Найти автора

```http
GET /authors/{author_name}
```

Возвращает информацию об авторе.

---

### Получить автора вместе со всеми его книгами

```http
GET /authors/{author_name}/books
```

Пример ответа:

```json
{
    "id": 1,
    "name": "J. R. R. Tolkien",
    "books": [
        {
            "id": 1,
            "title": "The Hobbit",
            "note": "Fantasy"
        },
        {
            "id": 2,
            "title": "The Lord of the Rings",
            "note": "Fantasy"
        }
    ]
}
```

---

### Удалить автора и все его книги

```http
DELETE /authors/{author_name}
```

Удаляет автора и связанные с ним книги.

---

# 🔗 SQLAlchemy Relationships

Главная учебная часть проекта — работа со связями между ORM-моделями.

Пример связи:

```python
class AuthorOrm(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    books: Mapped[list["BookOrm"]] = relationship(
        back_populates="author"
    )


class BookOrm(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    note: Mapped[str]

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id")
    )

    author: Mapped["AuthorOrm"] = relationship(
        back_populates="books"
    )
```

Теперь SQLAlchemy позволяет обращаться к связанным объектам:

```python
book.author
```

Получить автора книги.

```python
author.books
```

Получить все книги автора.

При этом сама база данных хранит связь через:

```text
books.author_id → authors.id
```

---

# ⚙️ Установка и запуск

## 1. Клонировать репозиторий

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
```

Перейти в директорию проекта:

```bash
cd BookAPI
```

---

## 2. Создать виртуальное окружение

### macOS / Linux

```bash
python3 -m venv .venv
```

Активировать:

```bash
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
```

Активировать:

```bash
.venv\Scripts\activate
```

---

## 3. Установить зависимости

```bash
pip install -r requirements.txt
```

---

## 4. Настроить PostgreSQL

Создайте базу данных PostgreSQL и укажите данные для подключения в `.env`.

Пример:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=your_password
DB_NAME=book_api
```

> Не добавляйте `.env` в Git. Файл с секретными данными должен находиться в `.gitignore`.

---

## 5. Запустить приложение

```bash
uvicorn app.main:app --reload
```

После запуска API будет доступен по адресу:

```text
http://127.0.0.1:8000
```

---

# 📖 Swagger

FastAPI автоматически создаёт интерактивную документацию API.

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 🎯 Что было изучено

В процессе создания проекта были отработаны:

- FastAPI
- REST API
- CRUD
- PostgreSQL
- SQLAlchemy ORM
- Async SQLAlchemy
- Pydantic
- Foreign Key
- One-to-Many relationships
- `relationship`
- `back_populates`
- Вложенные Pydantic-модели
- Поиск данных через SQLAlchemy
- Работа с несколькими связанными таблицами
- Удаление связанных данных
- Разделение проекта на модули
- Работа с `.env`
- Swagger / OpenAPI

---

# 💡 Цель проекта

Проект создан для закрепления навыков разработки backend-приложений на Python.

Основной акцент сделан на понимании того, как **FastAPI взаимодействует с PostgreSQL через SQLAlchemy ORM**, а также как реализуются связи между сущностями приложения.

---

## 📌 Статус

**Учебный проект завершён.**

Следующий этап обучения — более сложные backend-проекты с использованием PostgreSQL, FastAPI, SQLAlchemy, аутентификации, Docker и архитектурных подходов.