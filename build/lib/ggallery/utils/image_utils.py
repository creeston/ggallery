from PIL import Image
from io import BytesIO


def create_thumbnail(image_data, height: int):
    image = Image.open(BytesIO(image_data))
    aspect_ratio = image.width / image.height
    new_width = int(height * aspect_ratio)
    image.thumbnail((new_width, height), resample=Image.Resampling.BILINEAR)

    thumbnail_data = BytesIO()
    image.save(thumbnail_data, format="JPEG")
    thumbnail_data.seek(0)
    return thumbnail_data
