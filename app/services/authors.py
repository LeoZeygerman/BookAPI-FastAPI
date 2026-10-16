from sqlalchemy.ext.asyncio import AsyncSession
from app.models.authors import AuthorsOrm
from app.schemas.authors import CreateAuthor


async def create_author(session: AsyncSession, author: CreateAuthor) -> AuthorsOrm:
    new_author =  AuthorsOrm(
        author_name = author.author_name
        )
    session.add(new_author)
    await session.commit()
    return new_author