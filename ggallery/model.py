from typing import List, Optional
from pydantic import BaseModel, Field, model_validator, root_validator


class ThumbnailsConfig(BaseModel):
    height: int


class StorageConfig(BaseModel):
    type: str  # "local", "azure-blob", "s3", ...


class LocalStorageConfig(StorageConfig):
    type: str = "local"
    path: str


class AzureBlobStorageConfig(StorageConfig):
    type: str = "azure-blob"
    container: str
    connection_string: str


class OutputConfig(BaseModel):
    path: str
    index: Optional[str] = "index.html"


class PhotoConfig(BaseModel):
    filename: str
    thumbnail: str

    title: Optional[str] = None
    date: Optional[str] = None
    order: Optional[int] = None
    description: Optional[str] = None


class AlbumConfig(BaseModel):
    title: str
    subtitle: Optional[str] = None
    cover: Optional[str] = None

    source: Optional[str] = None
    photos: Optional[List[PhotoConfig]] = None

    @model_validator(mode="before")
    def check_folder_or_photos(cls, values):
        folder, photos = values.get("source"), values.get("photos")
        if folder and photos:
            raise ValueError("Use either 'folder' or 'photos', not both.")

        if not folder and not photos:
            raise ValueError("Either 'folder' or 'photos' must be provided.")
        return values

    id: Optional[int] = None


class GalleryConfig(BaseModel):
    title: str
    subtitle: Optional[str] = None
    thumbnail: ThumbnailsConfig = Field(default=ThumbnailsConfig(height=800))
    data_source: LocalStorageConfig | AzureBlobStorageConfig
    storage: LocalStorageConfig | AzureBlobStorageConfig
    output: OutputConfig
    albums: List[AlbumConfig] = Field(default_factory=list)
