from datetime import UTC

import arrow
from sqlmodel import Session

from app.apis.utils import utils
from app.models.urls import UrlsBase

EXAMPLE_URL = "https://www.google.com"


async def inject_initial_data(*, session: Session) -> None:
    url_obj: UrlsBase = UrlsBase(
        original_url=EXAMPLE_URL,
        short_url=utils.generate_url_uuid(EXAMPLE_URL),
        expiration_date=arrow.utcnow().shift(days=30).astimezone(UTC),
    )

    session.add(url_obj)
    session.commit()

    session.refresh(url_obj)
