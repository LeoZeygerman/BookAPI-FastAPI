from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.books import CreateBook


async def create_book(session: AsyncSession, book: CreateBook):
    pass