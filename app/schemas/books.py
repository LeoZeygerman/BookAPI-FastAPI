from pydantic import BaseModel, Field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.genres import ResponseGenreForBook
    from app.schemas.reviews import ResponseReview
    from app.schemas.authors import ResponseAuthorForBook
    
    
class CreateBook(BaseModel):
    book_title: str
    description: str = Field(min_length=10, max_length=150)

class ResponseBookForAuthor(BaseModel):
    book_title: str
    description: str
    genres: list['ResponseGenreForBook']
    
    
class ResponseBook(BaseModel):
    id: int
    book_title: str
    description: str
    author: 'ResponseAuthorForBook'
    genres: list['ResponseGenreForBook']
    reviews: list['ResponseReview']
    
    
class ResponseBookForGenres(BaseModel):
    id: int
    book_title: str
    

class UpdateBook(BaseModel):
    book_title: str | None
    description: str | None = Field(min_length=10, max_length=150)
    author: str | None
    genre: list[str] | None
    reviews: list[str] | None = Field(min_length=10, max_length=250)