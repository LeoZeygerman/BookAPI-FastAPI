from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.database import SessionDep
from app.models.genres import GenresOrm
from app.schemas.genres import CreateGenre, ResponseGenre

router = APIRouter(prefix='/genres', tags=['Жанры'])

@router.post('/', summary='Создать жанр', response_model=ResponseGenre)
async def create_genre(session: SessionDep, genre: CreateGenre):
    new_genre = GenresOrm(
        genre_title = genre.genre_title
    )
    session.add(new_genre)
    await session.commit()
    return new_genre


@router.get('/{genre_title}', summary='Найти жанр по названию', response_model=ResponseGenre)
async def get_genre_by_title(session: SessionDep, genre_title: str):
    genre = await session.scalar(
        select(GenresOrm)
        .where(GenresOrm.genre_title == genre_title)
        .options(
            selectinload(GenresOrm.books_with_genres)
        )
    )
    if genre is None:
        raise HTTPException(status_code=404, detail='Жанр не найден!')
    return genre


@router.get('/', summary='Получить все жанры', response_model=list[ResponseGenre])
async def get_all_genres(session: SessionDep):
    genres = await session.scalars(
        select(GenresOrm)
    )
    if len[genres] == 0:
        raise HTTPException(status_code=404, detail='Нет жанров!')
    return genres