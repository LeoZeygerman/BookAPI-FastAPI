from fastapi import APIRouter

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
