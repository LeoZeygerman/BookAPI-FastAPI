from fastapi import APIRouter
from app.database import SessionDep
from app.schemas.books import CreateBook, ResponseBook, ResponseBookForReviewCount, UpdateBook
from app.schemas.genres import ResponseGenre
from app.services.books import *


router = APIRouter(prefix='/books', tags=['Книги'])


@router.post('/', summary='Добавить книгу', response_model=ResponseBook)
async def create_book_router(session: SessionDep, book: CreateBook):
    new_book = await create_book(session, book)
    return new_book


@router.get('/{book_title}', summary='Получить книгу по названию' ,response_model=ResponseBook)
async def get_book_by_title_router(session: SessionDep, book_title: str):
    book = await get_book_by_title(session, book_title)
    return book


@router.get('/', summary='Получить все книги', response_model=list[ResponseBook])
async def get_all_books_router(session: SessionDep):
    books = await get_all_books(session)
    return books


@router.patch('/{book_title}', summary='Изменить книгу', response_model=ResponseBook)
async def update_book_router(session: SessionDep, data: UpdateBook, book_title: str):
    book = await update_book(session, data, book_title)
    return book


@router.delete('/{book_title}', summary='Удалить книгу')
async def delete_book_router(session: SessionDep, book_title: str):
    book = await delete_book(session, book_title)
    return book


@router.get('/genre/{genre_title}', summary='Поиск книг по жанру', response_model=list[ResponseGenre])
async def get_book_by_genre_router(session: SessionDep, genre_title: str):
    genre_with_books = await get_book_by_genre(session, genre_title)
    return genre_with_books


@router.get('/', summary='Самые обсуждаемые книги', response_model=list[ResponseBookForReviewCount])
async def get_most_reviewed_books_router(session: SessionDep):
    books = await get_most_reviewed_books(session)
    return books