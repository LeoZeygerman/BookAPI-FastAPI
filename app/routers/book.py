from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.database import SessionDep
from app.schemas import CreateBook, ResponseBook, ResponseAuthorWithBooks, UpdateBook
from app.models import BookOrm, AuthorOrm

router = APIRouter(prefix='/book', tags=['Книги'])

@router.post('/', summary='Добавить книгу', response_model= ResponseBook)
async def create_book(session: SessionDep, book: CreateBook ):
    query = select(AuthorOrm).where(AuthorOrm.name == book.author.name)
    result = await session.execute(query)
    author = result.scalar_one_or_none()

    if author is None:
        author = AuthorOrm(
            name = book.author.name
        )
        session.add(author)

    new_book = BookOrm(
        title = book.title,
        note = book.note,
        author = author
    )
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book


@router.get('/all', summary='Показать все книги', response_model = list[ResponseBook])
async def get_all(session: SessionDep):
    query = select(BookOrm)
    result = await session.execute(query)
    books = result.scalars().all()
    return books


@router.get('/{book_id}', summary='Найти книгу по id', response_model= ResponseBook)
async def get_book_by_id(session: SessionDep, book_id: int):
    query = select(BookOrm).where(BookOrm.id == book_id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail='Книга не найдена!')
    return book


@router.get('/{author_name}', summary='Показать все книги автора', response_model=ResponseAuthorWithBooks)
async def get_author_with_books(session: SessionDep, author_name: str):
    query = select(AuthorOrm).where(AuthorOrm.name == author_name)
    result = await session.execute(query)
    author = result.scalar_one_or_none()

    if not author:
        raise HTTPException(status_code=404, detail='Автор не найден!')
    return author


@router.patch('/{book_id}', summary='Изменить книгу', response_model=ResponseBook)
async def edit_book(session: SessionDep, book_id: int, book: UpdateBook):
    query = select(BookOrm).where(BookOrm.id == book_id)
    result = await session.execute(query)
    db_book = result.scalar_one_or_none()

    if not db_book:
        raise HTTPException(status_code=404, detail='Книга не найдена!')
    
    if book.title is not None:
        db_book.title = book.title
    if book.note is not None:
        db_book.note = book.note

    await session.commit()
    await session.refresh(db_book)
    return db_book


@router.delete()