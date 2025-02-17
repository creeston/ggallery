from .base_favicon_provider import BaseFaviconProvider
from .fontawesome_favicon_provider import FontAwesomeFaviconProvider
from .local_favicon_provider import LocalFaviconProvider


def get_favicon_provider(name: str) -> BaseFaviconProvider:
    if name == "fontawesome":
        return FontAwesomeFaviconProvider()
    elif name == "local":
        return LocalFaviconProvider()
    else:
        raise ValueError(f"Unsupported favicon provider: {name}")
