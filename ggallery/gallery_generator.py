from logging import Logger
import os
from pathlib import Path

from .docker import DockerImageBuilder
from .model import GalleryConfig, PhotoConfig, RendererParameters, OutputConfig
from .storage import BaseStorageProvider, BaseSourceDataProvider
from .image import ThumbnailCreator
from .favicon import BaseFaviconProvider
from .renderers import BaseRenderer


class GalleryGenerator:
    def __init__(
        self,
        source_storage_provider: BaseSourceDataProvider,
        target_storage_provider: BaseStorageProvider,
        thumbnail_creator: ThumbnailCreator,
        favicon_provider: BaseFaviconProvider | None,
        renderer: BaseRenderer,
        logger: Logger,
    ) -> None:
        self.source_storage_provider = source_storage_provider
        self.target_storage_provider = target_storage_provider
        self.thumbnail_creator = thumbnail_creator
        self.favicon_provider = favicon_provider
        self.renderer = renderer
        self.logger = logger

    def create_gallery(self, gallery: GalleryConfig) -> None:
        albums = gallery.albums
        thumbnail_height = gallery.thumbnail.height
        actual_thumbnail_height = thumbnail_height * 2  # Double the height for better quality

        for album in albums:
            self.logger.info(f"Processing album {album.title}.")
            if album.source is None:
                continue

            images = self.source_storage_provider.list_images(album.source)
            photos: list[PhotoConfig] = []
            source_catalog = album.source
            target_catalog = album.source

            for image_name in images:
                thumbnail_name = self.thumbnail_creator.create_thumbnail_name(image_name, actual_thumbnail_height)

                image_uri = self.target_storage_provider.file_exists(target_catalog, image_name)
                thumbnail_uri = self.target_storage_provider.file_exists(target_catalog, thumbnail_name)

                if not thumbnail_uri or not image_uri:
                    image = self.source_storage_provider.get_image_data(source_catalog, image_name)

                    if not image_uri:
                        self.logger.info(f"Uploading image {image_name} to storage.")
                        image_uri = self.target_storage_provider.upload_image(image, target_catalog, image_name)

                    if not thumbnail_uri:
                        thumbnail = self.thumbnail_creator.create_thumbnail(image, actual_thumbnail_height)
                        self.logger.info(f"Uploading thumbnail {thumbnail_name} to storage.")
                        thumbnail_uri = self.target_storage_provider.upload_image(
                            thumbnail, target_catalog, thumbnail_name
                        )

                photo = PhotoConfig(filename=image_uri, thumbnail=thumbnail_uri)
                if album.photos is not None:
                    existing_photo_metadata = next((p for p in album.photos if p.source == image_name), None)
                    if existing_photo_metadata:
                        photo = existing_photo_metadata
                        photo.filename = image_uri
                        photo.thumbnail = thumbnail_uri

                photos.append(photo)

            if album.cover is not None:
                thumbnail_name = self.thumbnail_creator.create_thumbnail_name(album.cover, actual_thumbnail_height)
                album.cover = self.target_storage_provider.file_exists(target_catalog, thumbnail_name)

            album.photos = photos

        output_config = gallery.output
        favicon_url = self.__get_favicon_url(gallery)

        render_parameters = RendererParameters(
            albums=albums,
            base_url=self.target_storage_provider.base_url(),
            thumbnail_height=thumbnail_height,
            title=gallery.title,
            subtitle=gallery.subtitle,
            favicon=favicon_url,
            template_parameters=gallery.template.parameters,
        )

        self.logger.info("Rendering gallery website.")
        rendered_files = self.renderer.render(render_parameters)
        if not isinstance(rendered_files, list):
            rendered_files = [rendered_files]
        for rendered_file in rendered_files:
            self.__write_content_to_output_directory(output_config.path, rendered_file.name, rendered_file.content)

        if gallery.docker is not None:
            docker_image_builder = DockerImageBuilder(gallery.docker.host, self.logger)
            docker_image_builder.build_docker_image(
                gallery.docker.image_name,
                gallery.docker.image_version,
                output_config.path,
            )

    def __write_content_to_output_directory(self, output_path: str, file_name: str, content: bytes | str) -> None:
        output_directory = Path(output_path)
        file_path = output_directory / file_name
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if isinstance(content, str):
            with file_path.open("w") as f:
                f.write(content)
        elif isinstance(content, bytes):
            with file_path.open("wb") as f:
                f.write(content)

    def __get_favicon_url(self, gallery: GalleryConfig) -> str | None:
        favicon_config = gallery.favicon
        output_config = gallery.output
        favicon_url = None
        if favicon_config is not None and self.favicon_provider is not None:
            favicon = self.favicon_provider.get_favicon(favicon_config)
            if favicon.url is not None:
                favicon_url = favicon.url
            elif favicon.content is not None and favicon.file_type is not None:
                favicon_name = f"favicon.{favicon.file_type}"
                self.__write_content_to_output_directory(output_config.path, favicon_name, favicon.content)
                favicon_url = favicon_name
        return favicon_url
