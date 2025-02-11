from ..model import FaviconConfig
from .base_favicon_provider import BaseFaviconProvider, Favicon

import requests


class FontAwesomeFaviconProvider(BaseFaviconProvider):
    def get_favicon(self, config: FaviconConfig) -> Favicon:
        url = f"https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6/svgs/solid/{config.name}.svg"
        # fetch the content of the favicon
        response = requests.get(url)
        response.raise_for_status()
        return Favicon(url=None, content=response.content, file_type="svg")

        return Favicon(
            url=f"https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6/svgs/solid/{config.name}.svg",
            content=None,
        )
