from pydantic import BaseModel

class CreateAuthor(BaseModel):
    name: str

class CreateBook(BaseModel):
    title: str
    note: str
    author: CreateAuthor


class ResponseBook(BaseModel):
    id: int
    title: str
    note: str
    author: str

class ResponseAuthorWithBooks(BaseModel):
    id: int
    name: str
    books: list[ResponseBook]

class UpdateBook(BaseModel):
    title: str | None = None
    note: str | None = None