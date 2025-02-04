import os
from dotenv import load_dotenv

from config import load_config
from providers import get_provider
from utils.image_utils import create_thumbnail
from utils.template_utils import render_template

load_dotenv()


def list_images(container_client, folder: str):
    image_blobs = []
    for blob in container_client.list_blobs(folder):
        if blob.name.lower().endswith((".png", ".jpg", ".jpeg")) and "thumbnails/" not in blob.name.lower():
            image_blobs.append(blob.name)

    return image_blobs


def create_thumbnail_name(image_path: str, height: int) -> str:
    *folders, filename = image_path.split("/")
    filename_without_extension = filename.split(".")[0]
    return f"{'/'.join(folders)}/thumbnails/{filename_without_extension}_{height}.jpg"


def main():
    config = load_config("gallery.yaml")
    data_source = config["data_source"]
    provider = get_provider(data_source)

    albums = config["albums"]
    thumbnail_config = config.get("thumbnail", {"height": 800})
    thumbnail_height = thumbnail_config["height"]

    for album in albums:
        images = provider.list_images(album["folder"])
        images_with_thumbnails = []
        for image_blob_name in images:
            thumbnail_blob_name = create_thumbnail_name(image_blob_name, thumbnail_height)
            if not provider.file_exists(thumbnail_blob_name):
                image_data = provider.get_image_data(image_blob_name)
                thumbnail = create_thumbnail(image_data, thumbnail_height)
                provider.upload_image(thumbnail, thumbnail_blob_name)
            images_with_thumbnails.append((image_blob_name, thumbnail_blob_name))
        album["images"] = images_with_thumbnails

    output_config = config.get("output", {"path": "docs", "index": "index.html"})
    if "index" not in output_config:
        output_config["index"] = "index.html"
    rendered_html = render_template(albums, provider.base_url, config["title"], config["subtitle"])

    os.makedirs(output_config["path"], exist_ok=True)
    with open(f"{output_config['path']}/{output_config['index']}", "w") as f:
        f.write(rendered_html)


if __name__ == "__main__":
    main()
