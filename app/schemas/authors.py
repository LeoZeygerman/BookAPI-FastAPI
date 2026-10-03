from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.books import ResponseBookForAuthor

class CreateAuthor(BaseModel):
    author_name: str
    

class ResponseAuthor(BaseModel):
    id: int
    author_name: str
    authors_book: list['ResponseBookForAuthor']
    
    model_config = ConfigDict(from_attributes=True)
    

class UpdateAuthor(BaseModel):
    author_name: str | None
    authors_book: list[str] | None
