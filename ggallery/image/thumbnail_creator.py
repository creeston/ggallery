from io import BytesIO
from PIL import Image, ImageOps
from io import BytesIO


class ThumbnailCreator:
    def create_thumbnail_name(self, image_uri: str, height: int) -> str:
        filename_without_extension = image_uri.split(".")[0]
        return f"{filename_without_extension}_thumbnail_{height}.jpg"

    def create_thumbnail(self, image_data, height: int) -> bytes:
        image = Image.open(BytesIO(image_data))
        image = ImageOps.exif_transpose(image)
        if image is None:
            raise ValueError("Invalid image data.")
        aspect_ratio = image.width / image.height
        new_width = int(height * aspect_ratio)
        image.thumbnail((new_width, height), resample=Image.Resampling.BILINEAR)
        thumbnail_data = BytesIO()
        image.save(thumbnail_data, format="JPEG")
        thumbnail_data.seek(0)
        thumbnail_data = thumbnail_data.read()
        return thumbnail_data
