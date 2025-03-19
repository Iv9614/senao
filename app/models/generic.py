from typing import Any
from typing import Generic
from typing import TypeVar

import arrow
from pydantic import BaseModel
from sqlmodel import Field

_T = TypeVar("_T", bound=Any)


class Message(BaseModel):
    pass


class SuccessMessage(Message, Generic[_T]):
    data: _T
    datetime: str = Field(default_factory=lambda: arrow.utcnow().datetime.isoformat())
