from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING
from app.schemas.books import ResponseGenreForBook


class ResponseBookForAuthor(BaseModel):
    book_title: str
    description: str
    genres: list[ResponseGenreForBook]

    model_config = ConfigDict(from_attributes=True)


class CreateAuthor(BaseModel):
    author_name: str
    

class ResponseAuthor(BaseModel):
    id: int
    author_name: str
    authors_books: list[ResponseBookForAuthor]
    
    model_config = ConfigDict(from_attributes=True)
    

class UpdateAuthor(BaseModel):
    author_name: str | None
    authors_book: list[str] | None


class ResponseAuthorForBook(BaseModel):
    author_name: str

    model_config = ConfigDict(from_attributes=True)