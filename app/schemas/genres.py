from pydantic import BaseModel, ConfigDict

   
class ResponseBookForGenres(BaseModel):
    id: int
    book_title: str

    model_config = ConfigDict(from_attributes=True)


class CreateGenre(BaseModel):
    genre_title: str
    
    
class ResponseGenre(BaseModel):
    id: int
    genre_title: str
    books_with_genres: list[ResponseBookForGenres]

    model_config = ConfigDict(from_attributes=True)
    
    
class UpdateGenre(BaseModel):
    genre_title: str | None