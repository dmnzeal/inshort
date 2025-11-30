from os import getenv
from datetime import datetime, timezone, timedelta
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import Session, select

from app.database import engine
from app.models.user import User, UserRead


load_dotenv()
SECRET_KEY = getenv("JWT_SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def create_access_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    data.update({"exp": expire})
    access_token = jwt.encode(data, SECRET_KEY, "HS256")
    return access_token


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    username = payload.get("username")
    if username is None:
        raise HTTPException(status_code=401)
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()
        if user is None:
            raise HTTPException(status_code=401)
        return UserRead.model_validate(user)
