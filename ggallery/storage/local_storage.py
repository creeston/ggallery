import os

from ..model import LocalStorageConfig
from .base_provider import BaseSourceDataProvider, BaseStorageProvider


class LocalSourceDataProvider(BaseSourceDataProvider):
    def __init__(self, config: LocalStorageConfig):
        if config.path is None:
            raise ValueError("Local storage path not found.")
        self.path = config.path

    def list_images(self, folder: str) -> list:
        images = []
        for filename in os.listdir(os.path.join(self.path, folder)):
            images.append(filename)
        return images

    def get_image_data(self, directory: str, image_name: str) -> bytes:
        with open(os.path.join(self.path, directory, image_name), "rb") as f:
            return f.read()


class LocalStorageProvider(BaseStorageProvider):
    """Storing images locally in same directory as index.html."""

    def __init__(self, config: LocalStorageConfig):
        if config.path is None:
            raise ValueError("Local storage path not found.")
        self.path = config.path

    def upload_image(self, image_data: bytes, directory, image_name) -> str:
        os.makedirs(os.path.join(self.path, directory), exist_ok=True)
        with open(os.path.join(self.path, directory, image_name), "wb") as f:
            f.write(image_data)
        return os.path.join(directory, image_name).replace("\\", "/")

    def file_exists(self, directory: str, image_name: str) -> str | None:
        file_path = os.path.join(directory, image_name)
        if os.path.exists(os.path.join(self.path, file_path)):
            return file_path.replace("\\", "/")
        return None

    def base_url(self) -> str:
        return ""  # Local storage does not have a base URL, files are stored in the same directory as index.html
