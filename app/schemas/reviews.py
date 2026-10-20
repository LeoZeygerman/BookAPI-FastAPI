from pydantic import BaseModel, ConfigDict, Field
from app.schemas.genres import ResponseBookForGenres


class CreateReview(BaseModel):
    user_name: str
    reviewed_book: str
    review: str = Field(min_length=10, max_length=250)


class ResponseReview(BaseModel):
    user_name: str
    reviewed_book: ResponseBookForGenres
    review: str

    model_config = ConfigDict(from_attributes=True)

    
class UpdateReview(BaseModel):
    user_name: str | None = None
    reviewed_book: str | None = None
    review: str | None = Field(default=None,min_length=10, max_length=250)