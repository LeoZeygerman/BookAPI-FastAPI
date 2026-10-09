from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.models.base import Base
from app.routers.reviews import router as review_router
from app.routers.genres import router as genre_router
from app.routers.authors import router as author_router
from app.routers.books import router as book_router
from app.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(book_router)
app.include_router(author_router)
app.include_router(genre_router)
app.include_router(review_router)