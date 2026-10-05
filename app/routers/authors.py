from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.database import SessionDep
from app.models.authors import AuthorsOrm
from app.schemas.authors import CreateAuthor, ResponseAuthor

router = APIRouter(prefix='/author', tags=['Автор'])

@router.post('/', summary='Создать автора', response_model=ResponseAuthor)
async def create_author(session: SessionDep, author: CreateAuthor):
    new_author = AuthorsOrm(
        author_name = author.author_name
    )
    session.add(new_author)
    await session.commit()
    return new_author


@router.get('/{author_name}', summary='Получить автора по имени')
async def get_author_by_name(session: SessionDep, author_name: str):
    author = await session.scalar(
        select(AuthorsOrm)
        .where(
            AuthorsOrm.author_name == author_name
        )
    )
    if author is None:
        raise HTTPException(status_code=404, detail='Автор не найден')
    return author