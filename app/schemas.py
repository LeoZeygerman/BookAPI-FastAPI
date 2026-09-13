from pydantic import BaseModel, ConfigDict

class CreateAuthor(BaseModel):
    name: str

class CreateBook(BaseModel):
    title: str
    note: str
    author: CreateAuthor

class ResponseAuthor(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class ResponseBook(BaseModel):
    id: int
    title: str
    note: str
    author: ResponseAuthor

    model_config = ConfigDict(from_attributes=True)

class ResponseAuthorWithBooks(BaseModel):
    id: int
    name: str
    books: list[ResponseBook]

class UpdateBook(BaseModel):
    title: str | None = None
    note: str | None = None