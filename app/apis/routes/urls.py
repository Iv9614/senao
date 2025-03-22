import uuid
from datetime import UTC
from logging import Logger
from logging import getLogger

import arrow
from fastapi import APIRouter
from fastapi import status
from sqlmodel import select
from yarl import URL

from app.apis.deps.session import SessionDep
from app.apis.deps.urls_process import GetCurrentUrl
from app.apis.deps.urls_process import GetShortUrl

# from app.apis.deps.urls_process import get_url
from app.models.generic import SuccessMessage
from app.models.urls import CreateURL
from app.models.urls import GetURLPublic
from app.models.urls import UpdateUrlSchema
from app.models.urls import UrlsBase

router = APIRouter(prefix="/urls", tags=["urls"])


logger: Logger = getLogger(__name__)


def generate_url_uuid(url: str) -> str:
    original_url: URL = URL(url)

    short_url_host: uuid = uuid.uuid3(uuid.NAMESPACE_DNS, url).hex[:10]
    short_url: str = f"{original_url.scheme}://senao/{short_url_host}"

    return short_url


@router.patch("/{url_id}", status_code=status.HTTP_204_NO_CONTENT)
async def patch_expire_time(session: SessionDep, current_url: GetCurrentUrl, update_url_in: UpdateUrlSchema) -> None:
    """
    Update URL expiration date or maybe others balalala...
    """
    current_url.sqlmodel_update(update_url_in.model_dump())

    session.add(current_url)
    session.commit()

    session.refresh(current_url)

    logger.info(f"Successful update URL expired date: {current_url}")  # noqa: G004


# Create Short URL
@router.post("/shorten", response_model=SuccessMessage[UrlsBase])
async def shorten_url(session: SessionDep, shorten_url_in: CreateURL) -> UrlsBase:
    """
    Create Short URL and url can't be duplicated.
    """
    url: UrlsBase = session.exec(select(UrlsBase).where(UrlsBase.original_url == shorten_url_in.original_url)).first()

    if url:
        logger.error("URL is existed, can't be duplicated.")

        raise ValueError("URL is existed,  can't be duplicated.")

    update: dict = {
        "short_url": generate_url_uuid(shorten_url_in.original_url),
        "expiration_date": arrow.utcnow().shift(days=30).astimezone(UTC),
    }

    db_obj = UrlsBase.model_validate(shorten_url_in, update=update)

    session.add(db_obj)
    session.flush([db_obj])
    session.commit()
    session.refresh(db_obj)

    logger.info(f"Successful create short URL: {db_obj}")  # noqa: G004

    return SuccessMessage(data=db_obj)


# Redirect to Original URL
@router.get("/", response_model=SuccessMessage[GetURLPublic])
async def redirect_url(current_url: GetShortUrl) -> GetURLPublic:
    """
    Redirect to Original URL
    """
    return SuccessMessage(data=current_url)
