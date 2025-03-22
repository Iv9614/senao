from sqlmodel import Field
from sqlmodel import SQLModel

from .common import DatetimeMixin


class UserBase(SQLModel):
    username: str | None = Field(nullable=False, index=True, max_length=2048)


class Users(UserBase, DatetimeMixin, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
