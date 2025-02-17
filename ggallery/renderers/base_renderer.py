from abc import abstractmethod, ABC
from ..model import RenderedFile, RendererParameters


class BaseRenderer(ABC):
    @abstractmethod
    def render(self, parameters: RendererParameters) -> list[RenderedFile] | RenderedFile:
        raise NotImplementedError
