from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.models.books import BooksOrm   

class AuthorsOrm(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_name: Mapped[str]

    authors_books: Mapped[list['BooksOrm']] = relationship(
        back_populates='author'
        )