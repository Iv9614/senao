from datetime import datetime

from pydantic import BaseModel
from pydantic import HttpUrl
from pydantic import field_validator


# Input Schema
class URLRequest(BaseModel):
    original_url: HttpUrl

    @field_validator("original_url", mode="before")
    @classmethod
    def check_length(cls, v: str) -> str:
        if len(v) > 2048:
            raise ValueError("URL is invalid, due to length is too long.")

        return v


# Output Schema
class URLResponse(BaseModel):
    short_url: str = ""
    expiration_date: datetime = None
    success: bool
    reason: str = None
