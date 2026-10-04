from pydantic import BaseModel
from typing import TYPE_CHECKING
from app.schemas.books import ResponseBookForGenres

class CreateGenre(BaseModel):
    genre_title: str


class ResponseGenreForBook(BaseModel):
    genre_title: str
    
    
class ResponseGenre(BaseModel):
    id: int
    genre_title: str
    books_with_genres: list[ResponseBookForGenres]
    
    
class UpdateGenre(BaseModel):
    genre_title: str | None
    book_with_genres: list[str] | None 