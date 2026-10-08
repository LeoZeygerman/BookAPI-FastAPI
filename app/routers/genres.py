from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.database import SessionDep
from app.models.genres import GenresOrm
from app.schemas.genres import CreateGenre, ResponseGenre, UpdateGenre

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
        .options(
            selectinload(GenresOrm.books_with_genres)
        )
    )
    if len(genres.all()) == 0:
        raise HTTPException(status_code=404, detail='Нет жанров!')
    return genres.all()


@router.patch('/{genre_title}', summary='Изменить жанр', response_model=ResponseGenre)
async def update_genre(session: SessionDep, genre_title: str, data: UpdateGenre):
    genre = await session.scalar(
        select(GenresOrm)
        .where(GenresOrm.genre_title == genre_title)
    )
    if genre is None:
        raise HTTPException(status_code=404, detail='Жанр не найден!')
    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(genre, key, value)
    await session.commit()
    await session.refresh(genre)
    return genre


@router.delete('/{genre_title}', summary='Удалить жанр')
async def delete_genre(session: SessionDep, genre_title: str):
    genre = await session.scalar(
        select(GenresOrm)
        .where(GenresOrm.genre_title == genre_title)
    )
    if genre is None:
        raise HTTPException(status_code=404, detail='Жанр не найден!')
    await session.delete(genre)
    await session.commit()
    return {'msg': f'Жанр {genre_title} удален!'}