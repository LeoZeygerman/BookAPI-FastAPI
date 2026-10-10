from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.models.authors import AuthorsOrm
from app.models.books import BooksOrm
from app.schemas.authors import CreateAuthor, ResponseAuthor, UpdateAuthor

router = APIRouter(prefix='/author', tags=['Автор'])

@router.post('/', summary='Создать автора', response_model=ResponseAuthor)
async def create_author(session: SessionDep, author: CreateAuthor):
    new_author = AuthorsOrm(
        author_name = author.author_name
    )
    session.add(new_author)
    await session.commit()
    return new_author


@router.get('/{author_name}', summary='Получить автора по имени', response_model=ResponseAuthor)
async def get_author_by_name(session: SessionDep, author_name: str):
    author = await session.scalar(
        select(AuthorsOrm)
        .where(
            AuthorsOrm.author_name == author_name
        )
        .options(selectinload(AuthorsOrm.authors_books))
    )
    if author is None:
        raise HTTPException(status_code=404, detail='Автор не найден')
    return author


@router.get('/', summary='Получить всех авторов', response_model=list[ResponseAuthor])
async def get_all_authors(session: SessionDep):
    authors = await session.scalars(
        select(AuthorsOrm)
        .options(selectinload(AuthorsOrm.authors_books))
    )
    return authors


@router.patch('/{author_name}', summary='Изменить автора', response_model=ResponseAuthor)
async def update_author(session: SessionDep, data: UpdateAuthor, author_name: str):
    author = await session.scalar(
        select(AuthorsOrm)
        .where(AuthorsOrm.author_name == author_name)
        .options(selectinload(AuthorsOrm.authors_books))
    )
    if author is None:
        raise HTTPException(status_code=404, detail='Автор не найден!')
    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(author, key, value)
    await session.commit()
    await session.refresh(author)
    return author
    

@router.delete('/{author_name}', summary='Удалить автора')
async def delete_author(session: SessionDep, author_name: str):
    author = await session.scalar(
        select(AuthorsOrm)
        .where(AuthorsOrm.author_name == author_name)
    )
    if author is None:
        raise HTTPException(status_code=404, detail='Автор не найден')
    await session.delete(author)
    await session.commit()
    return {'msg': f'Автор {author_name} удален!'}


@router.get('/', summary='Топ 5 авторов по количеству книг.', response_model=list[ResponseAuthor])
async def get_top_five_authors(session: SessionDep):
    authors = await session.execute(
        select(
            AuthorsOrm.id,
            func.count(BooksOrm.id)
        )
        .group_by(BooksOrm.author_id)
        .join(AuthorsOrm, BooksOrm.author_id == AuthorsOrm.id)
        .order_by(func.count(BooksOrm).desc())
        .limit(5)
    )
    if len(authors.all()) == 0:
        raise HTTPException(status_code=404, detail='Авторов нет')