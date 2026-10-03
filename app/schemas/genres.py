from pydantic import BaseModel

class ResponseGenreForBook(BaseModel):
    genre_title: str