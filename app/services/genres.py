from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.exception import NotFoundError
from app.models.genres import GenresOrm
from app.schemas.genres import CreateGenre, UpdateGenre


async def create_genre(session: AsyncSession, genre: CreateGenre):
    new_genre = GenresOrm(
        genre_title = genre.genre_title
    )

    session.add(new_genre)
    await session.flush()
    await session.commit()
    return await get_genre_by_title(session, genre.genre_title)


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


async def update_genre(session: AsyncSession, data: UpdateGenre, genre_title: str):
    genre = await session.scalar(
        select(GenresOrm)
        .where(GenresOrm.genre_title == genre_title)
        .options(
            selectinload(GenresOrm.books_with_genres)
        )
    )
    if genre is None:
        raise NotFoundError(f'Жанр {genre_title} не найден!')

    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(genre, field, value)

    await session.flush()
    await session.commit()
    return genre


async def delete_genre(session: AsyncSession, genre_title: str):
    genre = await session.scalar(
        select(GenresOrm)
        .where(GenresOrm.genre_title == genre_title)
    )
    if genre is None:
        raise NotFoundError(f'Жанр {genre_title} не найден!')

    await session.delete(genre)
    await session.commit()
    return {'msg': f'Жанр {genre_title} удален!'}



