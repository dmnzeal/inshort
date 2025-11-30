from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
import shortuuid

from app.database import engine
from app.models.url import Url, UrlCreate
from app.auth import get_current_user
from app.models.user import User


router = APIRouter(tags=["Url Shortener"])


@router.post("/shorten", status_code=201)
async def shorten(
    urlCreate: UrlCreate, current_user: Annotated[User, Depends(get_current_user)]
):
    with Session(engine) as session:
        hash = shortuuid.ShortUUID().random(length=6)
        new_url = Url(user_id=current_user.id, url=str(urlCreate.url), hash=hash)
        session.add(new_url)
        session.commit()
        session.refresh(new_url)
        return new_url


@router.get("/detail/{hash}", status_code=200)
async def detail(hash: str, current_user: Annotated[User, Depends(get_current_user)]):
    with Session(engine) as session:
        statement = select(Url).where(Url.hash == hash)
        results = session.exec(statement)
        url = results.first()
        if url is None:
            raise HTTPException(status_code=404)
        if url.user_id != current_user.id:
            raise HTTPException(status_code=403)
        return url


@router.delete("/delete/{hash}", status_code=204)
async def delete(hash: str, current_user: Annotated[User, Depends(get_current_user)]):
    with Session(engine) as session:
        statement = select(Url).where(Url.hash == hash)
        results = session.exec(statement)
        url = results.first()
        if url is None:
            raise HTTPException(status_code=404)
        if url.user_id != current_user.id:
            raise HTTPException(status_code=403)
        session.delete(url)
        session.commit()


@router.get("/{hash}", status_code=301)
async def redirect(hash: str):
    with Session(engine) as session:
        statement = select(Url).where(Url.hash == hash)
        results = session.exec(statement)
        url = results.first()
        if url is None:
            raise HTTPException(status_code=404)
        url.visits += 1
        session.add(url)
        session.commit()
        return RedirectResponse(url=url.url, status_code=301)
