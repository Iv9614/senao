import uuid

from yarl import URL


def generate_url_uuid(url: str) -> str:
    original_url: URL = URL(url)

    short_url_host: uuid = uuid.uuid3(uuid.NAMESPACE_DNS, url).hex[:10]
    short_url: str = f"{original_url.scheme}://senao/{short_url_host}"

    return short_url
