from fastapi import APIRouter
from sqlalchemy import select
from app.database import SessionDep
from app.models.authors import AuthorsOrm
from app.models.books import BooksOrm
from app.models.genres import GenresOrm
from app.schemas.books import CreateBook, ResponseBook 


router = APIRouter(prefix='/', tags=['Книги'])


@router.post('/', summary='Добавить книгу', response_model=ResponseBook)
async def create_book(session: SessionDep, book: CreateBook):
    new_author = await session.scalar(
        select(AuthorsOrm)
        .where(AuthorsOrm.author_name == book.author)
    )
    if new_author is None:
        new_author = AuthorsOrm(
            author_name = book.author
        )
        session.add(new_author)
    new_genres = []
    for genre in book.genres:
        new_genre = await session.scalar(
            select(GenresOrm)
            .where(GenresOrm.genre_title == genre)
        )
        if new_genre is None:
            new_genre = GenresOrm(
                genre_title = genre
            )
        new_genres.append(new_genre)

    new_book = BooksOrm(
        book_title = book.book_title,
        description = book.description,
        author = new_author,
        geners = new_genres

    )
    session.add(new_book)
    await session.commit()
    return new_book


@router.get('/{book_title}', summary='Получить книгу по названию' ,response_model=ResponseBook)
async def get_book_by_title(session: SessionDep, book_title: str):
    book = await session.scalar(
        select(BooksOrm)
        .where(
            BooksOrm.book_title == book_title
        )
    )
    return book