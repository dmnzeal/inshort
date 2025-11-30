from typing import List

from sqlmodel import Relationship, SQLModel, Field

from app.models.url import UrlRead


class UserBase(SQLModel):
    username: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str
    urls: List["Url"] = Relationship(back_populates="user")


class UserRegisterOrLogin(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    urls: List[UrlRead] = []


class Token(SQLModel):
    access_token: str
    token_type: str
