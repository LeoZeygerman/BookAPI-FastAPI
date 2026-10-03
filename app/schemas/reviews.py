from pydantic import BaseModel, Field
from typing import TYPE_CHECKING


class ResponseReview(BaseModel):
    user_name: str
    review: str = Field(min_length=10, max_length=250)