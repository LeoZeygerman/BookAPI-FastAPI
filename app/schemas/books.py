from pydantic import BaseModel
from app.schemas.genres import ResponseGenreForBook

class ResponseBookForAuthor(BaseModel):
    book_title: str
    description: str
    genres: list[ResponseGenreForBook]