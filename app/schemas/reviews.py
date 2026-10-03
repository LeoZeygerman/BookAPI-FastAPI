from pydantic import BaseModel, Field
from typing import TYPE_CHECKING


class CreateReview(BaseModel):
    user_name: str
    review: str = Field(min_length=10, max_length=250)

class ResponseReview(BaseModel):
    user_name: str
    review: str
    
    
class UpdateReview(BaseModel):
    user_name: str | None
    review: str | None = Field(min_length=10, max_length=250)