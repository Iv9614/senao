from logging import Logger
from logging import getLogger

from fastapi import APIRouter

from app.models.generic import SuccessMessage
from app.models.urls import URLRequest

router = APIRouter(prefix="", tags=["Urls"])


logger: Logger = getLogger(__name__)


# Create Short URL
@router.post("/shorten", response_model=SuccessMessage)
async def shorten_url(request: URLRequest) -> None:
    pass


# Redirect to Original URL
@router.get("/{short_code}")
async def redirect_url(short_code: str) -> None:
    pass
