from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import AsyncSession
from app.exception import NotFoundError
from app.models.genres import GenresOrm
from app.schemas.genres import CreateGenre


async def create_genre(session: AsyncSession, genre: CreateGenre):
    new_genre = GenresOrm(
        genre_title = genre.genre_title
    )
    
    session.add(new_genre)
    await session.flush()
    await session.commit()
    return new_genre


async def get_genre_by_title(session: AsyncSession, genre_title: str):
    genre = await session.scalar(
        select(GenresOrm)
        .where(GenresOrm.genre_title == genre_title)
        .options(
            selectinload(GenresOrm.books_with_genres)
        )
    )

    if genre is None:
        raise NotFoundError(f'Жанр {genre_title} не найден!')
    return genre


async def get_all_genres(session: AsyncSession):
    result = await session.scalars(
        select(GenresOrm)
        .options(
            selectinload(GenresOrm.books_with_genres)
        )
    )
    genres = result.all()

    if len(genres) == 0:
        raise NotFoundError(f'Жанры не найдены!')
    return genres