from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.database import SessionDep
from app.models.books import BooksOrm
from app.models.reviews import ReviewsOrm
from app.schemas.reviews import CreateReview, ResponseReview, UpdateReview

router = APIRouter(prefix='/reviews', tags=['Обзоры'])


@router.post('/', summary='Добавить обзор', response_model=ResponseReview)
async def create_review(session: SessionDep, review: CreateReview):
    book = await session.scalar(
        select(BooksOrm)
        .where(BooksOrm.book_title == review.reviewed_book)
    )
    if book is None:
        raise HTTPException(status_code=404, detail='Книга не найдена!')
    new_review = ReviewsOrm(
        user_name = review.user_name,
        reviewed_book = book,
        review = review.review
    )
    session.add(new_review)
    await session.commit()
    return new_review


@router.get('/{user_name}', summary='Получить обзоры по имени человека', response_model=list[ResponseReview])
async def get_review_by_user_name(session: SessionDep, user_name: str):
    review = await session.scalar(
        select(ReviewsOrm)
        .where(ReviewsOrm.user_name == user_name)
        .options(ReviewsOrm.reviewed_book)
    )
    if review is None:
        raise HTTPException(status_code=404, detail='Обзор не найден')
    return review


@router.get('/', summary='Получить все обзоры', response_model=list[ResponseReview])
async def get_all_reviews(session: SessionDep):
    reviews = await session.execute(
        select(ReviewsOrm)
        .options(ReviewsOrm.reviewed_book)
    )
    if len(reviews.all()):
        raise HTTPException(status_code=404, detail='Обзоров нет')
    return reviews.all()


@router.patch('/update-genre/{review_id}', summary='Изменить обзор', response_model=ResponseReview)
async def update_genre(session: SessionDep, review_id: int, data: UpdateReview):
    review = await session.scalar(
        select(ReviewsOrm)
        .where(ReviewsOrm.id == review_id)
        .options(ReviewsOrm.reviewed_book)
    )
    changes = data.model_dump(exclude_unset=True)
    simple_field = {'user_name','review'}
    for key,value in changes.items():
        if key in simple_field:
            setattr(review, key, value)
    if 'reviewed_book' in changes:
        reviewed_book = await session.scalar(
            select(BooksOrm)
            .where(BooksOrm.book_title == changes['reviewed_book'])
        )
        if reviewed_book is None:
            raise HTTPException(status_code=404, detail='Книга не найдена!')
        setattr(review, 'reviewed_book', reviewed_book)
    await session.commit()
    await session.refresh(review)
    return review

