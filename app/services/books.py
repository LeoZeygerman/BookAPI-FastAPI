from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.exception import NotFoundError
from app.models.books import BooksOrm
from app.schemas.books import CreateBook
from app.services.lookups import get_or_create_genre, get_or_create_author
from sqlalchemy.orm import selectinload


async def create_book(session: AsyncSession, book: CreateBook):
    author = get_or_create_author(session, book.author)
    genres = []
    for genre_title in book.genres:
        genre = get_or_create_genre(session, genre_title)
        genres.append(genre)

    new_book = BooksOrm(
        book_title = book.book_title,
        description = book.description,
        author = author,
        genres = genres
    )

    session.add(new_book)
    await session.commit()
    return new_book


async def get_book_by_title(session: AsyncSession, book_title: str):
    book = await session.scalar(
        select(BooksOrm)
        .where(BooksOrm.book_title == book_title)
        .options(
            selectinload(BooksOrm.genres),
            selectinload(BooksOrm.reviews),
            selectinload(BooksOrm.author)
            )
    )

    if book is None:
        raise NotFoundError(f'Книга не найдена!')
    return book