from pydantic import BaseModel, ConfigDict, Field
from typing import TYPE_CHECKING
from app.schemas.reviews import ResponseReview


class ResponseGenreForBook(BaseModel):
    genre_title: str

    model_config = ConfigDict(from_attributes=True)


class ResponseAuthorForBook(BaseModel):
    author_name: str

    model_config = ConfigDict(from_attributes=True)
    
    
class CreateBook(BaseModel):
    book_title: str
    description: str = Field(min_length=10, max_length=150)
    author: str
    genres: list[str]

    
class ResponseBook(BaseModel):
    id: int
    book_title: str
    description: str
    author: ResponseAuthorForBook
    genres: list[ResponseGenreForBook]
    reviews: list[ResponseReview]

    model_config = ConfigDict(from_attributes=True)
    

class UpdateBook(BaseModel):
    book_title: str | None
    description: str | None = Field(min_length=10, max_length=150)
    author: str | None
    genre: list[str] | None
