from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class BookGenreOrm(Base):
    __tablename__ = 'genre_book'

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id', ondelete='CASCADE'))
    genre_id: Mapped[int] = mapped_column(ForeignKey('genres.id', ondelete='CASCADE'))