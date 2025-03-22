from datetime import datetime

from pydantic import BaseModel
from pydantic import field_validator
from sqlalchemy_utils.types.arrow import ArrowType
from sqlmodel import Field
from sqlmodel import SQLModel

from .common import ArrowPydanticV2
from .common import DatetimeMixin


class URL(SQLModel):
    original_url: str


class GetURLPublic(URL):
    pass


class CreateURLResponse(BaseModel):
    short_url: str = ""
    expiration_date: datetime = None
    success: bool
    reason: str = None


# Input Schema
class CreateURL(URL):
    @field_validator("original_url", mode="before")
    @classmethod
    def check_length(cls, v: str) -> str:
        if len(v) > 2048:
            raise ValueError("URL is invalid, due to length is too long.")

        return v


# Output Schema


class UrlsBase(SQLModel, DatetimeMixin, table=True):
    __tablename__ = "urls"

    id: int = Field(default=None, primary_key=True)

    original_url: str | None = Field(nullable=False, index=True, max_length=2048)
    short_url: str | None = Field(nullable=False, index=True, max_length=2048)

    expiration_date: ArrowPydanticV2 | None = Field(nullable=True, sa_type=ArrowType, default=None)


class UpdateUrlSchema(SQLModel):
    expiration_date: ArrowPydanticV2 | None = Field(nullable=True, sa_type=ArrowType, default=None)
