from abc import abstractmethod, ABC
from dataclasses import dataclass
from ..model import FaviconConfig


@dataclass
class Favicon:
    url: str | None
    content: bytes | None
    file_type: str | None = None


class BaseFaviconProvider(ABC):
    @abstractmethod
    def get_favicon(self, config: FaviconConfig) -> Favicon:
        pass
