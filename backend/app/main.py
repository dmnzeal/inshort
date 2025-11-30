from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import url_shortener, qr_generator, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router=url_shortener.router)
app.include_router(router=qr_generator.router)
app.include_router(router=users.router)
