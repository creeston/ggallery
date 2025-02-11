from abc import ABC, abstractmethod


class BaseStorageProvider(ABC):
    @abstractmethod
    def upload_image(self, image_data: bytes, directory: str, image_name: str) -> str:
        pass

    @abstractmethod
    def file_exists(self, directory: str, image_name: str) -> str | None:
        pass

    @abstractmethod
    def base_url(self) -> str:
        pass


class BaseSourceDataProvider(ABC):
    @abstractmethod
    def list_images(self, folder: str) -> list:
        pass

    @abstractmethod
    def get_image_data(self, directory: str, image_name: str) -> bytes:
        pass
