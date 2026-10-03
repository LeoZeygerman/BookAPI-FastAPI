from pydantic import BaseModel
from app.schemas.books import ResponseBookForAuthor

class CreateAuthor(BaseModel):
    author_name: str
    

class ResponseAuthor(BaseModel):
    id: int
    author_name: str
    authors_book: list[ResponseBookForAuthor]