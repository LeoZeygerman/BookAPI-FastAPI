from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import AsyncSession
from app.exception import NotFoundError
from app.models.books import BooksOrm
from app.models.reviews import ReviewsOrm
from app.schemas.reviews import CreateReview, UpdateReview


async def create_review(session: AsyncSession, review: CreateReview):
    book = await session.scalar(
        select(BooksOrm)
        .where(BooksOrm.book_title == review.reviewed_book)
    )
    if book is None:
        raise NotFoundError(f'Книга для обзора не найдена!')

    new_review = ReviewsOrm(
        user_name = review.user_name,
        reviewed_book = book,
        review = review.review
    )
    session.add(new_review)
    await session.commit()
    return new_review


async def get_review_by_username(session: AsyncSession, user_name: str):
    result = await session.scalars(
        select(ReviewsOrm)
        .where(ReviewsOrm.user_name == user_name)
        .options(
            selectinload(ReviewsOrm.reviewed_book)
        )
    )
    reviews = result.all()

    if len(reviews) == 0:
        raise NotFoundError(f'Обзоров от {user_name} нет!')
    return reviews


async def get_all_reviews(session: AsyncSession):
    result = await session.scalars(
        select(ReviewsOrm)
        .options(
            selectinload(ReviewsOrm.reviewed_book)
        )
    )
    reviews = result.all()

    if len(reviews) == 0:
        raise NotFoundError(f'Обзоров нет!')
    return reviews


async def update_review(session: AsyncSession, data: UpdateReview, user_name: str):
    review = get_review_by_username(session, user_name)
    changes = data.model_dump(exclude_unset=True)
    await _apply_changes(session, review, changes)
    await session.flush()
    await session.commit()
    return review


async def _apply_reviewed_book(session: AsyncSession, review: ReviewsOrm, book_title: str):
    book = await session.scalar(
        select(BooksOrm)
        .where(BooksOrm.book_title == book_title)
    )
    if book is None:
        raise NotFoundError(f'Книга не найдена!')
    review.reviewed_book = book


def _apply_simple(field: str | int):
    async def setter(session: AsyncSession, review: ReviewsOrm, value: str):
        setattr(review, field, value)
    return setter


_FIELD_HANDLERS = {
    'user_name': _apply_simple('user_name'),
    'reviewed_book': _apply_reviewed_book,
    'review': _apply_simple('review')
}


async def _apply_changes(session: AsyncSession, review: ReviewsOrm, changes: dict):
    for field, value in changes.items():
        handler = _FIELD_HANDLERS.get(field)
        if handler is None:
            raise NotFoundError(f'Параметр {field} не найден!')
        await handler(session, review, value)