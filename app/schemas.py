from pydantic import BaseModel, ConfigDict

class CreateBook(BaseModel):
    title: str
    author: str
    release_date: int

class UpdateBook(BaseModel):
    title: str | None
    author: str | None
    release_date: int | None

class ResponseBook(BaseModel):
    id: int
    title: str
    author: str
    release_date: int
    model_config = ConfigDict(from_attributes=True)