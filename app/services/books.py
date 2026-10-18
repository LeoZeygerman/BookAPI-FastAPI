from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.exception import NotFoundError
from app.models.books import BooksOrm
from app.models.genres import GenresOrm
from app.models.reviews import ReviewsOrm
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


async def get_all_books(session: AsyncSession):
    result = await session.scalars(
        select(BooksOrm)
        .options(
            selectinload(BooksOrm.author),
            selectinload(BooksOrm.reviews),
            selectinload(BooksOrm.genres)
        )
    )

    books = result.all()
    if len(books) is None:
        raise NotFoundError(f'Книг нет!')
    return books 


async def delete_book(session: AsyncSession, book_title: str):
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
        raise NotFoundError(f'Книга {book_title} не найдена!')

    await session.delete(book)
    await session.commit()
    return {'msg': f'Книга {book_title} удалена!'}


async def get_book_by_genre(session: AsyncSession, genre_title: str):
    genre_with_books = await session.scalars(
        select(GenresOrm)
        .where(GenresOrm.genre_title == genre_title)
        .options(
            selectinload(GenresOrm.books_with_genres)
        )
    )
    books = genre_with_books.all()

    if len(books) == 0:
        raise NotFoundError(f'Книги с жанорм {genre_title} не найдены!')
    return books


async def get_most_reviewed_books(session: AsyncSession):
    result = await session.execute(
        select(
            BooksOrm.id,
            func.count(ReviewsOrm.id).label('review_count')
        )
        .join(ReviewsOrm, ReviewsOrm.book_id == BooksOrm.id)
        .group_by(BooksOrm.id)
        .order_by(func.count(ReviewsOrm.id).desc())
        .limit(10)
    )
    books = result.mappings().all()
    return books