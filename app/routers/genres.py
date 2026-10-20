from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.database import SessionDep
from app.models.genres import GenresOrm
from app.schemas.genres import CreateGenre, ResponseGenre, UpdateGenre
from app.services.genres import *

router = APIRouter(prefix='/genres', tags=['Жанры'])

@router.post('/genres', summary='Создать жанр', response_model=ResponseGenre)
async def create_genre_router(session: SessionDep, genre: CreateGenre):
    new_genre = create_genre(session, genre)
    return new_genre


@router.get('/{genre_title}', summary='Найти жанр по названию', response_model=ResponseGenre)
async def get_genre_by_title_router(session: SessionDep, genre_title: str):
    genre = await get_genre_by_title(session, genre_title)
    return genre


@router.get('/', summary='Получить все жанры', response_model=list[ResponseGenre])
async def get_all_genres_router(session: SessionDep):
    genres = await get_all_genres(session)
    return genres


@router.patch('/{genre_title}', summary='Изменить жанр', response_model=ResponseGenre)
async def update_genre_router(session: SessionDep, genre_title: str, data: UpdateGenre):
    genre = await update_genre(session, data, genre_title)
    return genre


@router.delete('/{genre_title}', summary='Удалить жанр')
async def delete_genre_router(session: SessionDep, genre_title: str):
    genre = await delete_genre(session, genre_title)
    return genre