from azure.storage.blob import BlobServiceClient
from .base_provider import BaseSourceDataProvider, BaseStorageProvider
from ..model import AzureBlobStorageConfig


class AzureBlobSourceDataProvider(BaseSourceDataProvider):
    def __init__(self, config: AzureBlobStorageConfig):
        self.config = config
        if not self.config.connection_string:
            raise ValueError("Azure Storage connection string not found.")

        self.blob_service_client = BlobServiceClient.from_connection_string(self.config.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.config.container)
        self.base_url_value = self.container_client.url + "/"

    def list_images(self, folder: str) -> list:
        image_blobs = []
        for blob in self.container_client.list_blobs(folder):
            if blob.name.lower().endswith((".png", ".jpg", ".jpeg")) and "thumbnails/" not in blob.name.lower():
                image_blobs.append(blob.name)
        return image_blobs

    def get_image_data(self, directory: str, image_name: str) -> bytes:
        blob_client = self.container_client.get_blob_client(f"{directory}/{image_name}")
        return blob_client.download_blob().readall()


class AzureBlobStorageProvider(BaseStorageProvider):
    def __init__(self, config: AzureBlobStorageConfig):
        self.config = config
        if not self.config.connection_string:
            raise ValueError("Azure Storage connection string not found.")

        self.blob_service_client = BlobServiceClient.from_connection_string(self.config.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.config.container)
        self.base_url_value = self.container_client.url + "/"

    def upload_image(self, image_data, directory, image_name) -> str:
        blob_name = f"{directory}/{image_name}"
        if self.__blob_exists(blob_name):
            return blob_name
        blob_client = self.container_client.get_blob_client(f"{directory}/{image_name}")
        blob_client.upload_blob(image_data, overwrite=True)
        return blob_name

    def file_exists(self, directory: str, image_name: str) -> str | None:
        blob_name = f"{directory}/{image_name}"
        if self.__blob_exists(blob_name):
            return blob_name
        return None

    def __blob_exists(self, blob_name: str) -> bool:
        try:
            self.container_client.get_blob_client(blob_name).get_blob_properties()
            return True
        except:
            return False

    def base_url(self) -> str:
        return self.base_url_value
