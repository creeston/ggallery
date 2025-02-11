from .base_favicon_provider import Favicon, BaseFaviconProvider
from .fontawesome_favicon_provider import FontAwesomeFaviconProvider


def get_favicon_provider(name: str) -> BaseFaviconProvider:
    if name == "fontawesome":
        return FontAwesomeFaviconProvider()
    else:
        raise ValueError(f"Unsupported favicon provider: {name}")
