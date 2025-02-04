from .azure_blob import AzureBlobProvider


def get_provider(data_source_config):
    if data_source_config["type"] == "azure-blob":
        return AzureBlobProvider(data_source_config["container"])
    else:
        raise ValueError(f"Unsupported data source type: {data_source_config['type']}")
