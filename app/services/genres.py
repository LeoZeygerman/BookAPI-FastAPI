from app.database import AsyncSession
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
