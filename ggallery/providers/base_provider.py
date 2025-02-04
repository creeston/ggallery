from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    def list_images(self, folder: str):
        pass

    @abstractmethod
    def create_thumbnail(self, image_blob_name: str, height: int) -> None:
        pass

    @abstractmethod
    def get_image_data(self, image_blob_name: str) -> bytes:
        pass

    @abstractmethod
    def upload_image(self, image_data, image_blob_name) -> None:
        pass

    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        pass

    @property
    @abstractmethod
    def base_url(self):
        pass
