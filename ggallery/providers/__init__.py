from .azure_blob_storage import AzureBlobProvider
from .local_storage import LocalFileStorageProvider

from ..model import StorageConfig, LocalStorageConfig, AzureBlobStorageConfig


def get_provider(data_source_config: LocalStorageConfig | AzureBlobStorageConfig):
    if data_source_config.type == "azure-blob":
        return AzureBlobProvider(data_source_config)  # type: ignore
    elif data_source_config.type == "local":
        return LocalFileStorageProvider(data_source_config)  # type: ignore
    else:
        raise ValueError(f"Unsupported data source type: {data_source_config.type}")
