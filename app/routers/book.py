from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
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
        await session.flush()

    new_book = BookOrm(
        title = book.title,
        note = book.note,
        author = author
    )
    session.add(new_book)
    await session.commit()

    query = (
        select(BookOrm)
        .where(BookOrm.id == new_book.id)
        .options(selectinload(BookOrm.author))
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()

@router.get('/all', summary='Показать все книги', response_model = list[ResponseBook])
async def get_all(session: SessionDep):
    query = (
        select(BookOrm)
        .options(selectinload(BookOrm.author))
    )
    result = await session.execute(query)
    books = result.scalars().all()
    return books


@router.get('/{book_id}', summary='Найти книгу по id', response_model= ResponseBook)
async def get_book_by_id(session: SessionDep, book_id: int):
    query = (
        select(BookOrm)
        .where(BookOrm.id == book_id)
        .options(selectinload(BookOrm.author))
    )
    result = await session.execute(query)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail='Книга не найдена!')
    return book


@router.get('/{author_name}', summary='Показать все книги автора', response_model=ResponseAuthorWithBooks)
async def get_author_with_books(session: SessionDep, author_name: str):
    query = (
        select(AuthorOrm)
        .where(AuthorOrm.name == author_name)
        .options(joinedload(AuthorOrm.books))
    )
    result = await session.execute(query)
    author = result.scalar_one_or_none()

    if not author:
        raise HTTPException(status_code=404, detail='Автор не найден!')
    return author


@router.patch('/{book_id}', summary='Изменить книгу', response_model=ResponseBook)
async def edit_book(session: SessionDep, book_id: int, book: UpdateBook):
    query = (
        select(BookOrm)
        .where(BookOrm.id == book_id)
        .options(selectinload(BookOrm.author))
    )
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


@router.delete('/{book_id}', summary='Удалить книгу')
async def delete_book(session: SessionDep, book_id: int):
    query = (
        select(BookOrm)
        .where(BookOrm.id == book_id)
        .options(selectinload(BookOrm.author))
    )
    result = await session.execute(query)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail='Книга не найдена!')

    await session.delete(book)
    await session.commit()
    return f'Книга {book.title} удалена!'


@router.delete('/{author_name}', summary='Удалить автора и его книги')
async def delete_author_with_books(session: SessionDep, author_name: str):
    query = (
        select(AuthorOrm)
        .where(AuthorOrm.name == author_name)
        .options(joinedload(AuthorOrm.books))
    )
    result = await session.execute(query)
    author = result.scalar_one_or_none()

    if not author:
        raise HTTPException(status_code=404, detail='Автор не найден!')
    book_query = select(BookOrm).where(BookOrm.author == author)
    book_result = await session.execute(book_query)
    book = book_result.scalars().all()

    await session.delete(book)
    await session.delete(author)
    await session.commit()
    return f'Автор и все его книги удалены!'