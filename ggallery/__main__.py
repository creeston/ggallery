import os
import argparse

from dotenv import load_dotenv

from .model import GalleryConfig, PhotoConfig
from .config import load_config
from .providers import get_provider
from .utils.image_utils import create_thumbnail
from .utils.template_utils import render_template

load_dotenv()


class Arguments:
    file: str


def create_thumbnail_name(image_uri: str, height: int) -> str:
    filename_without_extension = image_uri.split(".")[0]
    return f"{filename_without_extension}_thumbnail_{height}.jpg"


def main(args: Arguments):
    if not os.path.exists(args.file):
        print(f"Configuration file {args.file} not found.")
        return

    config: GalleryConfig = load_config(args.file)

    source_config = config.data_source
    source_provider = get_provider(source_config)

    storage_config = config.storage
    storage_provider = get_provider(storage_config)

    albums = config.albums
    thumbnail_height = config.thumbnail.height

    for album in albums:
        if album.source is None:
            continue

        images = source_provider.list_images(album.source)
        photos: list[PhotoConfig] = []
        for image_name in images:
            thumbnail_name = create_thumbnail_name(image_name, thumbnail_height)

            image_uri = storage_provider.file_exists(album.source, image_name)
            thumbnail_uri = storage_provider.file_exists(album.source, thumbnail_name)

            if not thumbnail_uri or not image_uri:
                image = source_provider.get_image_data(album.source, image_name)

                if not image_uri:
                    image_uri = storage_provider.upload_image(image, album.source, image_name)

                if not thumbnail_uri:
                    thumbnail = create_thumbnail(image, thumbnail_height)
                    thumbnail_uri = storage_provider.upload_image(thumbnail, album.source, thumbnail_name)

            photos.append(PhotoConfig(filename=image_uri, thumbnail=thumbnail_uri))

        if album.cover is not None:
            album.cover = storage_provider.file_exists(album.source, album.cover)

        album.photos = photos

    output_config = config.output
    rendered_html = render_template(albums, storage_provider.base_url(), config.title, config.subtitle)
    os.makedirs(output_config.path, exist_ok=True)
    with open(f"{output_config.path}/{output_config.index}", "w") as f:
        f.write(rendered_html)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a static HTML photo gallery.", prog="ggallery")

    if not os.path.exists("gallery.yaml"):
        parser.add_argument("-f", "--file", help="Path to the configuration file", required=True)
    else:
        parser.add_argument("-f", "--file", help="Path to the configuration file", default="gallery.yaml")

    args: Arguments = parser.parse_args(namespace=Arguments)  # type: ignore
    main(args)
