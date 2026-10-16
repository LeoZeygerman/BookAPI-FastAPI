from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.authors import AuthorsOrm
from app.schemas.authors import CreateAuthor
from sqlalchemy.orm import selectinload


async def create_author(session: AsyncSession, author: CreateAuthor) -> AuthorsOrm:
    new_author =  AuthorsOrm(
        author_name = author.author_name
        )
    session.add(new_author)
    await session.commit()
    return new_author


async def get_author_by_name(session: AsyncSession, author_name: str):
    author = await session.scalar(
        select(AuthorsOrm)
        .where(AuthorsOrm.author_name == author_name)
        .options(selectinload(AuthorsOrm.authors_books))
    )
    return author