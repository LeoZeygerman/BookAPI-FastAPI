from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.books import BooksOrm

class ReviewsOrm(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(unique=True)
    review: Mapped[str]

    reviewed_book: Mapped['BooksOrm'] = relationship(
        back_populates='reviews'
    )