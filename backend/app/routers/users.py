from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from passlib.context import CryptContext

from app.database import engine
from app.models.user import Token, User, UserRegisterOrLogin, UserRead
from app.auth import create_access_token, get_current_user


router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["argon2"])


@router.post("/register", status_code=201)
async def register(payload: UserRegisterOrLogin):
    with Session(engine) as session:
        statement = select(User).where(User.username == payload.username)
        user = session.exec(statement).first()
        if user:
            raise HTTPException(status_code=409)
        password_hash = pwd_context.hash(payload.password)
        new_user = User(username=payload.username, password_hash=password_hash)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return UserRead.model_validate(new_user)


@router.post("/login")
async def login(payload: UserRegisterOrLogin) -> Token:
    with Session(engine) as session:
        statement = select(User).where(User.username == payload.username)
        user = session.exec(statement).first()
        if user is None:
            raise HTTPException(401)
        if not pwd_context.verify(payload.password, user.password_hash):
            raise HTTPException(401)
        access_token = create_access_token({"username": user.username})
        return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
async def me(current_user: Annotated[User, Depends(get_current_user)]) -> UserRead:
    return current_user
