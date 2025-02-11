from abc import abstractmethod, ABC
from ..model import RendererParameters


class BaseRenderer(ABC):
    @abstractmethod
    def render(self, parameters: RendererParameters) -> str:
        raise NotImplementedError
