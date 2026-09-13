from fastapi import APIRouter
from sqlalchemy import select
from app.database import SessionDep
from app.schemas import CreateBook, ResponseBook
from app.models import BookOrm, AuthorOrm

router = APIRouter(prefix='/book', tags=['Книги'])

@router.post('/', summary='Добавить книгу', response_model= ResponseBook)
async def create_book(session: SessionDep, book: CreateBook ):
    query = select(AuthorOrm).where(AuthorOrm.name == book.author.name)
    result = await session.execute(query)
    author = result.scalar_one_or_none()

    if author is None:
        author = AuthorOrm(
            name = book.author.name
        )
        session.add(author)

    new_book = BookOrm(
        title = book.title,
        note = book.note,
        author = author
    )
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book