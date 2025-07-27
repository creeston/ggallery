from ..model import FaviconConfig
from .base_favicon_provider import BaseFaviconProvider, Favicon


class LocalFaviconProvider(BaseFaviconProvider):
    def get_favicon(self, config: FaviconConfig) -> Favicon:
        with open(config.name, "rb") as file:
            file_extension = config.name.split(".")[-1]
            return Favicon(url=None, content=file.read(), file_type=file_extension)
