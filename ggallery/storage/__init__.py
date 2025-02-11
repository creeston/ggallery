from .azure_blob_storage import AzureBlobSourceDataProvider, AzureBlobStorageProvider
from .local_storage import LocalSourceDataProvider, LocalStorageProvider
from .base_provider import BaseSourceDataProvider, BaseStorageProvider

from ..model import LocalStorageConfig, AzureBlobStorageConfig


def get_source_provider(data_source_config: LocalStorageConfig | AzureBlobStorageConfig) -> BaseSourceDataProvider:
    if data_source_config.type == "azure-blob":
        return AzureBlobSourceDataProvider(data_source_config)  # type: ignore
    elif data_source_config.type == "local":
        return LocalSourceDataProvider(data_source_config)  # type: ignore
    else:
        raise ValueError(f"Unsupported data source type: {data_source_config.type}")


def get_storage_provider(storage_config: LocalStorageConfig | AzureBlobStorageConfig) -> BaseStorageProvider:
    if storage_config.type == "azure-blob":
        return AzureBlobStorageProvider(storage_config)  # type: ignore
    elif storage_config.type == "local":
        return LocalStorageProvider(storage_config)  # type: ignore
    else:
        raise ValueError(f"Unsupported storage type: {storage_config.type}")
