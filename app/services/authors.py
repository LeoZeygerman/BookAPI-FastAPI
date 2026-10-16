from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.exception import NotFoundError
from app.models.authors import AuthorsOrm
from app.models.books import BooksOrm
from app.schemas.authors import CreateAuthor, UpdateAuthor
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
    if author is None:
        raise NotFoundError(f'Автор не найден!')
    return author


async def get_all_authors(session: AsyncSession):
    result = await session.scalars(
        select(AuthorsOrm)
        .options(selectinload(AuthorsOrm.authors_books))
    )
    
    authors = result.all()
    if len(authors) == 0:
        raise NotFoundError(f'Авторов нет!')
    return authors


async def update_author(session: AsyncSession, data: UpdateAuthor, author_name: str):
    author = await session.scalar(
        select(AuthorsOrm)
        .where(AuthorsOrm.author_name == author_name)
        .options(selectinload(AuthorsOrm.authors_books))
    )
    if author is None:
        raise NotFoundError(f'Автор не найден!')
    
    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(author, key, value)

    await session.commit()
    await session.refresh(author)
    return author


async def delete_author(session: AsyncSession, author_name: str):
    author = await session.scalar(
        select(AuthorsOrm)
        .where(AuthorsOrm.author_name == author_name)
    )
    if author is None:
        raise NotFoundError(f'Автор не найден!')

    await session.delete(author)
    await session.commit()
    return {'msg': f'Автор {author_name} удален!'}


async def get_top_five_authors(session: AsyncSession):
    result = await session.execute(
        select(
            AuthorsOrm.author_name,
            func.array_agg(BooksOrm.book_title).label('book_title'),
            func.count(BooksOrm.id).label('book_count')
        )
        .group_by(AuthorsOrm.id)
        .join(BooksOrm, BooksOrm.author_id == AuthorsOrm.id)
        .order_by(func.count(BooksOrm.id).desc())
        .limit(5)
    )

    authors = result.mappings().all()
    if len(authors) == 0:
        raise NotFoundError(f'Авторов нет!')
    return authors


async def get_author_with_n_books(session: AsyncSession, book_count: int):
    result = await session.execute(
        select(
            AuthorsOrm.author_name,
            func.array_agg(BooksOrm.book_title).label('books_title'),
            func.count(BooksOrm.id).label('book_count')
        )
        .group_by(AuthorsOrm.id)
        .join(BooksOrm, BooksOrm.author_id == AuthorsOrm.id)
        .having(func.count(BooksOrm.id) == book_count)
    )

    authors = result.mappings().all()
    if len(authors) == 0:
        raise NotFoundError(f'Авторы с таким количеством книг не найдены!')

    return authors