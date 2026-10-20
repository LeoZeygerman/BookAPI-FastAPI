from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.authors import AuthorsOrm
from app.models.genres import GenresOrm


async def get_or_create_author(session: AsyncSession, author_name: str) -> GenresOrm:
    author = await session.scalar(
        select(AuthorsOrm)
        .where(AuthorsOrm.author_name == author_name)
    )
    if author is None:
        author = AuthorsOrm(
            author_name = author_name
        )
        session.add(author)
    return author


async def get_or_create_genre(session: AsyncSession, genre_title: str) -> GenresOrm:
    genre = await session.scalar(
        select(GenresOrm)
        .where(GenresOrm.genre_title == genre_title)
    )
    if genre is None:
        genre = GenresOrm(
            genre_title = genre_title
        )
        session.add(genre)
    return genre