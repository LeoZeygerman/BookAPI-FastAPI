from fastapi import APIRouter
from app.database import SessionDep
from app.schemas import CreateBook
from app.models import BookOrm, AuthorOrm

router = APIRouter(prefix='/book', tags=['Книги'])

@router.post('/', summary='Добавить книгу')
async def create_book(session: SessionDep, book: CreateBook ):
    new_author = AuthorOrm(name = book.author.name)
    if new_author.name not in AuthorOrm:
        session.add(new_author)
        await session.commit()
    new_book = BookOrm(title = book.title, note = book.note, author = new_author)