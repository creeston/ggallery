from azure.storage.blob import BlobServiceClient
from PIL import Image
from io import BytesIO
import os
from .base_provider import BaseProvider


class AzureBlobProvider(BaseProvider):
    def __init__(self, container_name: str):
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not self.connection_string:
            raise ValueError("Azure Storage connection string not found.")

        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)
        self.base_url = self.container_client.url + "/"

    def list_images(self, folder: str):
        image_blobs = []
        for blob in self.container_client.list_blobs(folder):
            if blob.name.lower().endswith((".png", ".jpg", ".jpeg")) and "thumbnails/" not in blob.name.lower():
                image_blobs.append(blob.name)
        return image_blobs

    def get_image_data(self, image_blob_name: str):
        blob_client = self.container_client.get_blob_client(image_blob_name)
        return blob_client.download_blob().readall()

    def upload_image(self, image_data, image_blob_name):
        blob_client = self.container_client.get_blob_client(image_blob_name)
        blob_client.upload_blob(image_data, overwrite=True)

    def file_exists(self, file_path: str) -> bool:
        try:
            self.container_client.get_blob_client(file_path).get_blob_properties()
            return True
        except:
            return False

    def create_thumbnail(self, image_blob_name: str, height: int):
        folder, filename = image_blob_name.split("/")
        filename_without_extension = filename.split(".")[0]
        thumbnail_blob_name = f"{folder}/thumbnails/{filename_without_extension}_{height}.jpg"

        try:
            self.container_client.get_blob_client(thumbnail_blob_name).get_blob_properties()
            return thumbnail_blob_name
        except:
            pass

        blob_client = self.container_client.get_blob_client(image_blob_name)
        image_data = blob_client.download_blob().readall()

        image = Image.open(BytesIO(image_data))
        aspect_ratio = image.width / image.height
        new_width = int(height * aspect_ratio)
        image.thumbnail((new_width, height), resample=Image.Resampling.BILINEAR)

        thumbnail_data = BytesIO()
        image.save(thumbnail_data, format="JPEG")
        thumbnail_data.seek(0)

        thumbnail_blob_client = self.container_client.get_blob_client(thumbnail_blob_name)
        thumbnail_blob_client.upload_blob(thumbnail_data, overwrite=True)

        return thumbnail_blob_name

    def base_url(self):
        return self.base_url
