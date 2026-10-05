from fastapi import APIRouter
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