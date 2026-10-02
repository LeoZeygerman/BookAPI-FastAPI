from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.books import BooksOrm

class GenresOrm(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(primary_key=True)
    genre_title: Mapped[str] = mapped_column(unique=True)

    books_with_genres: Mapped[list['BooksOrm']] = relationship(
        back_populates='genres',
        secondary='genre_book'
    )