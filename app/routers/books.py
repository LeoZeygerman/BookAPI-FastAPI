from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.models.authors import AuthorsOrm
from app.models.books import BooksOrm
from app.models.genres import GenresOrm
from app.schemas.books import CreateBook, ResponseBook, UpdateBook 


router = APIRouter(prefix='/books', tags=['Книги'])


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
    if book is None:
        raise HTTPException(status_code=404, detail='Книга с названием {book_title} не найдена!')
    return book


@router.get('/', summary='Получить все книги', response_model=list[ResponseBook])
async def get_all_books(session: SessionDep):
    books = await session.scalars(
        select(BooksOrm)
    )
    if books is None:
        raise HTTPException(status_code=404, detail='Книги не найдены')
    return books


@router.patch('/{book_title}', summary='Изменить книгу', response_model=ResponseBook)
async def update_book(session: SessionDep, data: UpdateBook, book_title: str):
    book = await session.scalar(
        select(BooksOrm)
        .where(BooksOrm.book_title == book_title)
        .options(selectinload(BooksOrm.author),
                 selectinload(BooksOrm.genres))
    )
    changes = data.model_dump(exclude_unset=True)
    simple_fields = {'book_title','description'}
    for key, value in changes.items():
        if key in simple_fields:
            setattr(book,key,value)

    if 'author' in changes:
        author = await session.scalar(
            select(AuthorsOrm)
            .where(AuthorsOrm.author_name == changes['author'])
        )
        if author is None:
            author = AuthorsOrm(
                author_name = changes['author']
            )
            session.add(author)
        setattr(book,'author', author)
    
    if 'genre' in changes:
        genres = []
        for genre in changes['genre']:
            db_genre = await session.scalar(
                select(GenresOrm)
                .where(GenresOrm.genre_title == genre)
            )
            if db_genre is None:
                db_genre = GenresOrm(
                    genre_title = genre
                )
                session.add(db_genre)
            genres.append(db_genre)
        setattr(book, 'genres', genres)

@router.delete('/{book_title}', summary='Удалить книгу')
async def delete_book(session: SessionDep, book_title: str):
    book = await session.scalar(
        select(BooksOrm)
        .where(BooksOrm.book_title == book_title)
    )
    if book is None:
        raise HTTPException(status_code=404, detail='Книга не найдена!')
    await session.delete(book)
    await session.commit()
    return {'msg': f'Книга {book_title} удалена!'}