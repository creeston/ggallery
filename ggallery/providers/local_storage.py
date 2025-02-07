from io import BytesIO
import os
import pathlib

from ..model import LocalStorageConfig
from .base_provider import BaseProvider


class LocalFileStorageProvider(BaseProvider):
    def __init__(self, config: LocalStorageConfig):
        self.config = config

    def list_images(self, folder: str) -> list:
        images = []
        for filename in os.listdir(os.path.join(self.config.path, folder)):
            images.append(filename)
        return images

    def get_image_data(self, directory: str, image_name: str) -> bytes:
        with open(os.path.join(self.config.path, directory, image_name), "rb") as f:
            return f.read()

    def upload_image(self, image_data: bytes, directory, image_name) -> str:
        os.makedirs(os.path.join(self.config.path, directory), exist_ok=True)
        with open(os.path.join(self.config.path, directory, image_name), "wb") as f:
            f.write(image_data)
        return os.path.join(directory, image_name)

    def file_exists(self, directory: str, image_name: str) -> str | None:
        file_path = os.path.join(directory, image_name)
        if os.path.exists(os.path.join(self.config.path, file_path)):
            return file_path
        return None

    def base_url(self) -> str:
        return pathlib.Path(self.config.path).as_uri()
