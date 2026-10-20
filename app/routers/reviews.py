from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.models.books import BooksOrm
from app.models.reviews import ReviewsOrm
from app.schemas.reviews import CreateReview, ResponseReview, UpdateReview
from app.services.reviews import *

router = APIRouter(prefix='/reviews', tags=['Обзоры'])


@router.post('/', summary='Добавить обзор', response_model=ResponseReview)
async def create_review_router(session: SessionDep, review: CreateReview):
    new_review = await create_review(session, review)
    return new_review


@router.get('/{user_name}', summary='Получить обзоры по имени человека', response_model=list[ResponseReview])
async def get_review_by_username_router(session: SessionDep, user_name: str):
    review = await get_review_by_username(session, user_name)
    return review


@router.get('/', summary='Получить все обзоры', response_model=list[ResponseReview])
async def get_all_reviews_router(session: SessionDep):
    reviews = await get_all_reviews(session)
    return reviews


@router.patch('/update-review/{review_id}', summary='Изменить обзор', response_model=ResponseReview)
async def update_review(session: SessionDep, username: str, data: UpdateReview):
    review = await update_review(session, data, username)
    return review

