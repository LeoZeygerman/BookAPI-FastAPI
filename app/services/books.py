from sqlalchemy.ext.asyncio import AsyncSession
from app.models.books import BooksOrm
from app.schemas.books import CreateBook
from app.services.lookups import get_or_create_genre, get_or_create_author


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