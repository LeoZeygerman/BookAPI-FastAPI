from sqlalchemy import ForeignKey

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.books import BooksOrm

class ReviewsOrm(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str]
    review: Mapped[str]

    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))

    reviewed_book: Mapped['BooksOrm'] = relationship(
        back_populates='reviews'
    )