from fastapi import APIRouter
from app.database import SessionDep
from app.schemas.authors import CreateAuthor, ResponseAuthor, ResponseAuthorForTops, UpdateAuthor
from app.services.authors import *

router = APIRouter(prefix='/author', tags=['Автор'])

@router.post('/', summary='Создать автора', response_model=ResponseAuthor)
async def create_author_router(session: SessionDep, author: CreateAuthor):
    new_author = await create_author(session, author)
    return new_author

    
@router.get('/{author_name}', summary='Получить автора по имени', response_model=ResponseAuthor)
async def get_author_by_name_router(session: SessionDep, author_name: str):
    author = await get_author_by_name(session, author_name)
    return author


@router.get('/get-all', summary='Получить всех авторов', response_model=list[ResponseAuthor])
async def get_all_authors_router(session: SessionDep):
    authors = await get_all_authors(session)
    return authors


@router.patch('/update/{author_name}', summary='Изменить автора', response_model=ResponseAuthor)
async def update_author_router(session: SessionDep, data: UpdateAuthor, author_name: str):
    author = await update_author(session, data, author_name)
    return author
    

@router.delete('/delete/{author_name}', summary='Удалить автора')
async def delete_author_router(session: SessionDep, author_name: str):
    author = await delete_author(session, author_name)
    return author


@router.get('/top', summary='Топ 5 авторов по количеству книг.', response_model=list[ResponseAuthorForTops])
async def get_top_five_authors_router(session: SessionDep):
    authors = await get_top_five_authors(session)
    return authors


@router.get('/book-count/{book_count}', summary='Получить авторов с N количеством книг', response_model=list[ResponseAuthorForTops])
async def get_author_with_n_books_router(session: SessionDep, book_count: int):
    authors = await get_author_with_n_books(session, book_count)
    return authors


@router.get('/avg', summary='Авторы с количеством книг больше среднего', response_model=list[ResponseAuthor])
async def get_authors_more_than_avg_router(session: SessionDep):
    authors = await get_authors_more_than_avg(session)
    return authors