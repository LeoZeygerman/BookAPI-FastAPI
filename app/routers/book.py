from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from schemas import CreateBook, ResponseBook, UpdateBook
from models import BookOrm
from database import SessionDep

router = APIRouter(
    prefix='/books',
    tags=['Книги']
)

@router.post('/', summary='Добавить книгу')
async def create_book(session: SessionDep, book: CreateBook):
    new_book = BookOrm(
        title = book.title,
        author = book.author,
        release_date = book.release_date
    )

    session.add(new_book)
    await session.commit()

    return {'msg': f'Книга {book.title} добавлена!'}


@router.get('/get_all', summary='Показать все книги', response_model=list[ResponseBook])
async def get_all_books(session: SessionDep):
    query = select(BookOrm)
    result = await session.execute(query)
    books = result.scalars().all()
    return books

@router.get('/{book_id}', summary='Показать одну книгу', response_model=ResponseBook)
async def get_book(book_id: int, session: SessionDep):
    query = select(BookOrm).where(BookOrm.id == book_id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail='Книга не найдена')
    return book

@router.delete('/{book_id}', summary='Удаление книги')
async def delete_book(book_id: int, session: SessionDep):
    query = select(BookOrm).where(BookOrm.id == book_id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail='Книга не найдена')
    await session.delete(book)
    await session.commit()
    return {'msg': f'Книга {book.title} удалена!'}

@router.patch('/{book_id}', summary='Изменить книгу', response_model= ResponseBook)
async def update_book(book_id: int, session: SessionDep, book: UpdateBook):
    query = select(BookOrm).where(BookOrm.id == book_id)
    result = await session.execute(query)
    db_book = result.scalar_one_or_none()
    if db_book is None:
        raise HTTPException(status_code=404, detail='Книга не найдена')
    if book.title is not None:
        db_book.title = book.title
    if book.author is not None:
        db_book.author = book.author
    if book.release_date is not None:
        db_book.release_date = book.release_date
    await session.commit()
    return db_book