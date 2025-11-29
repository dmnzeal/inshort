from sqlmodel import SQLModel, Field
from pydantic import HttpUrl, PositiveInt


class UrlBase(SQLModel):
    pass


class Url(UrlBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hash: str = Field(unique=True, index=True)
    visits: int = Field(default=0)
    url: str


class UrlCreate(UrlBase):
    url: HttpUrl
