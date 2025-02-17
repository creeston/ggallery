from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


class FaviconConfig(BaseModel):
    type: str  # "fontawesome", "local"
    name: str  # "camera-retro"


class ThumbnailsConfig(BaseModel):
    height: int


class TemplateConfig(BaseModel):
    url: str
    parameters: Optional[dict] = None


class StorageConfig(BaseModel):
    type: str  # "local", "azure-blob", "s3", ...


class LocalStorageConfig(StorageConfig):
    type: str = "local"
    path: str | None = None  # Path to the local folder, must be same as output path


class AzureBlobStorageConfig(StorageConfig):
    type: str = "azure-blob"
    container: str
    connection_string: str


class OutputConfig(BaseModel):
    path: str


class PhotoConfig(BaseModel):
    source: str | None = None
    filename: str | None = None
    thumbnail: str | None = None

    title: Optional[str] = None


class AlbumConfig(BaseModel):
    title: str
    subtitle: Optional[str] = None
    cover: Optional[str] = None

    source: Optional[str] = None
    photos: Optional[List[PhotoConfig]] = None

    @model_validator(mode="before")
    def check_folder_or_photos(cls, values):
        folder, photos = values.get("source"), values.get("photos")
        if not folder and not photos:
            raise ValueError("Either 'folder' or 'photos' must be provided.")
        return values

    id: Optional[int] = None


class GalleryConfig(BaseModel):
    title: str
    subtitle: Optional[str] = None
    favicon: Optional[FaviconConfig] = None
    template: TemplateConfig
    thumbnail: ThumbnailsConfig = Field(default=ThumbnailsConfig(height=400))
    data_source: LocalStorageConfig | AzureBlobStorageConfig
    data_storage: LocalStorageConfig | AzureBlobStorageConfig
    output: OutputConfig
    albums: List[AlbumConfig] = Field(default_factory=list)


class RendererParameters(BaseModel):
    albums: List[AlbumConfig]
    base_url: str
    thumbnail_height: int
    title: str
    subtitle: Optional[str]
    favicon: Optional[str]
    template_parameters: Optional[dict] = None


class RenderedFile(BaseModel):
    name: str
    content: bytes | str
