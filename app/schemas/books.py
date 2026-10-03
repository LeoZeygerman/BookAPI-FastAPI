from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.genres import ResponseGenreForBook
    from app.schemas.reviews import ResponseReview
    from app.schemas.authors import ResponseAuthorForBook

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