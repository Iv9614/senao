from datetime import UTC
from logging import Logger
from logging import getLogger
from typing import Annotated

import arrow
from fastapi import Depends
from sqlmodel import select

from app.apis.deps.session import SessionDep
from app.models.urls import UrlsBase

logger: Logger = getLogger(__name__)


def get_current_url(session: SessionDep, url_id: int) -> UrlsBase:
    url_obj: UrlsBase = session.exec(select(UrlsBase).where(UrlsBase.id == url_id)).first()

    if not url_obj:
        logger.error("URL is not existed")

        raise ValueError("URL is not existed.")

    return url_obj


GetCurrentUrl = Annotated[UrlsBase, Depends(get_current_url)]


def get_short_url(session: SessionDep, *, short_url: str) -> UrlsBase:
    url: UrlsBase = session.exec(select(UrlsBase).where(UrlsBase.short_url == short_url)).first()

    if not url:
        logger.error("URL is not existed")

        raise ValueError("URL is not existed.")

    if url.expiration_date < arrow.utcnow().astimezone(UTC):
        logger.error("URL is expired")

        raise ValueError("URL is expired.")

    return url


GetShortUrl = Annotated[UrlsBase, Depends(get_short_url)]
