from fastapi import APIRouter
from sqlalchemy import select
from app.database import SessionDep
from app.models.books import BooksOrm
from app.models.reviews import ReviewsOrm
from app.schemas.reviews import CreateReview, ResponseReview

router = APIRouter(prefix='/reviews', tags=['Обзоры'])


@router.post('/', summary='Добавить обзор', response_model=ResponseReview)
async def create_review(session: SessionDep, review: CreateReview):
    book = await session.scalar(
        select(BooksOrm)
        .where(BooksOrm.book_title == review.reviewed_book)
    )
    new_review = ReviewsOrm(
        user_name = review.user_name,
        reviewed_book = book,
        review = review.review
    )
    session.add(new_review)
    await session.commit()
    return new_review