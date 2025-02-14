import logging
import os
import argparse

from dotenv import load_dotenv

from .model import GalleryConfig, LocalStorageConfig
from .config import load_config
from .storage import get_source_provider, get_storage_provider
from .renderers import RendererImporter
from .favicon import get_favicon_provider
from .image import ThumbnailCreator
from .gallery_generator import GalleryGenerator

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger("ggallery")
logging.getLogger("azure.core").setLevel(logging.WARNING)


class Arguments:
    file: str


def main():
    parser = argparse.ArgumentParser(description="Generate a static HTML photo gallery.", prog="ggallery")

    if not os.path.exists("gallery.yaml"):
        parser.add_argument("-f", "--file", help="Path to the configuration file", required=True)
    else:
        parser.add_argument("-f", "--file", help="Path to the configuration file", default="gallery.yaml")

    args: Arguments = parser.parse_args(namespace=Arguments)  # type: ignore

    if not os.path.exists(args.file):
        print(f"Configuration file {args.file} not found.")
        return

    gallery: GalleryConfig = load_config(args.file)
    source_provider = get_source_provider(gallery.data_source)

    if isinstance(gallery.data_storage, LocalStorageConfig):
        gallery.data_storage.path = gallery.output.path

    target_provider = get_storage_provider(gallery.data_storage)
    favicon_provider = get_favicon_provider(gallery.favicon.type) if gallery.favicon is not None else None
    with RendererImporter(gallery.template.url) as renderer:
        thumbnail_creator = ThumbnailCreator()
        gallery_generator = GalleryGenerator(
            source_storage_provider=source_provider,
            target_storage_provider=target_provider,
            thumbnail_creator=thumbnail_creator,
            favicon_provider=favicon_provider,
            renderer=renderer,
            logger=logger,
        )

        gallery_generator.create_gallery(gallery)


if __name__ == "__main__":
    main()
