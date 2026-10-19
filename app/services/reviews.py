from sqlalchemy import select

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