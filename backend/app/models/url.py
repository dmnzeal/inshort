from sqlmodel import SQLModel, Field, Relationship
from pydantic import HttpUrl, PositiveInt


class UrlBase(SQLModel):
    pass


class Url(UrlBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="urls")
    hash: str = Field(unique=True, index=True)
    visits: int = Field(default=0)
    url: str


class UrlCreate(UrlBase):
    url: HttpUrl
    user_id: int


class UrlRead(UrlBase):
    id: int
    url: str
    visits: int
    hash: str
