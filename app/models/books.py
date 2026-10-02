from app.models.authors import AuthorsOrm
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.genres import GenresOrm
from app.models.reviews import ReviewsOrm

class BooksOrm(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    book_title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]

    reviews: Mapped[list['ReviewsOrm']] = relationship(
        back_populates='reviewed_books'
    )

    author: Mapped['AuthorsOrm'] = relationship(
        back_populates='authors_books'
    )

    genres: Mapped[list['GenresOrm']] = relationship(
        back_populates='books_with_genres',
        secondary='genre_book'
    )