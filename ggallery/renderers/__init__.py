from .nano_gallery_renderer import NanoGalleryTemplateRenderer
from .base_renderer import BaseRenderer


def get_renderer(name: str) -> BaseRenderer:
    if name == "nano-gallery":
        return NanoGalleryTemplateRenderer()
    else:
        raise ValueError(f"Unsupported data source type: {name}")
