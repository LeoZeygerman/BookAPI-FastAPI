from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import AsyncSession
from app.exception import NotFoundError
from app.models.books import BooksOrm
from app.models.reviews import ReviewsOrm
from app.schemas.reviews import CreateReview


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