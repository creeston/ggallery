from pathlib import Path
from unittest.mock import MagicMock
from ggallery.gallery_generator import GalleryGenerator
from ggallery.model import AlbumConfig, PhotoConfig, LocalStorageConfig, AzureBlobStorageConfig, RenderedFile, RendererParameters, OutputConfig
from ggallery.storage import get_source_provider, get_storage_provider
from ggallery.image import ThumbnailCreator
from ggallery.renderers import BaseRenderer
from azure.storage.blob import BlobServiceClient
from testcontainers.azurite import AzuriteContainer
from tests.gallery_config_factory import GalleryConfigFactory
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger("ggallery-tests")
logging.getLogger("azure.core").setLevel(logging.WARNING)


class TestGalleryGenerator:
    blob_container_name = "photos"

    def setup_method(self):
        self.thumbnail_creator = MagicMock()
        self.favicon_provider = MagicMock()
        self.logger = MagicMock()
        self.azurite_container = AzuriteContainer()
        self.azurite_container.start()
        client = BlobServiceClient.from_connection_string(
            self.azurite_container.get_connection_string(),
            api_version="2025-05-05"
        )
        client.create_container(self.blob_container_name, public_access="blob")

    def teardown_method(self):
        self.azurite_container.stop()

    def test_create_gallery_with_local_source_and_azure_target(self):
        script_directory = Path(__file__).parent
        assets_path = script_directory / "assets"

        gallery_config = GalleryConfigFactory().with_albums([
            AlbumConfig(
                title="test album",
                subtitle="test subtitle",
                source="album",
                cover="peter-herrmann-4cWu6XpOe58-unsplash.jpg",
                photos=[
                    PhotoConfig(
                        title="Peter Herrmann Photo",
                        filename="peter-herrmann-4cWu6XpOe58-unsplash.jpg",
                        source="peter-herrmann-4cWu6XpOe58-unsplash.jpg",
                    ),
                    PhotoConfig(
                        title="Peter Thomas Photo",
                        filename="peter-thomas-ep-6kGyBSXk-unsplash.jpg",
                        source="peter-thomas-ep-6kGyBSXk-unsplash.jpg",
                    ),
                    PhotoConfig(
                        title="Victor Rosario Photo",
                        filename="victor-rosario-f2SquFjpESg-unsplash.jpg",
                        source="victor-rosario-f2SquFjpESg-unsplash.jpg",
                    )
                ]
            )
        ]).with_data_source(
            LocalStorageConfig(path=assets_path.absolute().as_posix())
        ).with_data_storage(
            AzureBlobStorageConfig(container=self.blob_container_name, connection_string=self.azurite_container.get_connection_string())
        ).with_title(
            "Test Gallery"
        ).with_subtitle(
            "Test Subtitle"
        ).with_output(
            OutputConfig(
                path=assets_path.absolute().as_posix()
            )
        ).build()

        source_provider = get_source_provider(gallery_config.data_source)
        target_provider = get_storage_provider(gallery_config.data_storage)
        thumbnail_creator = ThumbnailCreator()
        renderer = RendererStub()

        gallery_generator = GalleryGenerator(
            source_storage_provider=source_provider,
            target_storage_provider=target_provider,
            thumbnail_creator=thumbnail_creator,
            favicon_provider=None,
            renderer=renderer,
            logger=logger,
        )

        gallery_generator.create_gallery(gallery_config)

        expected_export_file = assets_path / renderer.rendered_gallery_name
        assert expected_export_file.exists(), f"Expected export file {expected_export_file} does not exist"

        export_file_content = expected_export_file.read_text(encoding="utf-8")
        rendered_parameters = RendererParameters.model_validate_json(export_file_content)
        assert rendered_parameters.title == gallery_config.title
        assert rendered_parameters.subtitle == gallery_config.subtitle
        assert len(rendered_parameters.albums) == 1
        rendered_album = rendered_parameters.albums[0]
        config_album = gallery_config.albums[0]
        assert rendered_album.title == config_album.title
        assert rendered_album.subtitle == config_album.subtitle
        assert rendered_album.photos is not None
        assert config_album.photos is not None

        for rendered_photo, config_photo in zip(rendered_album.photos, config_album.photos):
            assert rendered_photo.filename is not None
            assert config_photo.filename is not None
            rendered_photo_url = rendered_parameters.base_url + rendered_photo.filename
            source_photo_path = assets_path / config_photo.filename

            rendered_photo_content = requests.get(rendered_photo_url).content
            source_photo_content = source_photo_path.read_bytes()
            assert rendered_photo_content == source_photo_content

        expected_export_file.unlink() 


class RendererStub(BaseRenderer):
    rendered_gallery_name = "rendered_gallery.json"

    def render(self, parameters: RendererParameters) -> list[RenderedFile] | RenderedFile:
        return RenderedFile(
            name=self.rendered_gallery_name, 
            content=parameters.model_dump_json(indent=4).encode("utf-8")
        )