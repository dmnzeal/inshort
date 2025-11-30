from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from passlib.context import CryptContext

from app.database import engine
from app.models.user import User, UserRegisterOrLogin, UserRead


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
