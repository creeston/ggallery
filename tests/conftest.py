import pytest
from .gallery_config_factory import GalleryConfigFactory

@pytest.fixture
def gallery_config():
    return GalleryConfigFactory().build()