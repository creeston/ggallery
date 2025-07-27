from ggallery.model import AlbumConfig, GalleryConfig, LocalStorageConfig, OutputConfig, TemplateConfig, ThumbnailsConfig


class GalleryConfigFactory:
    def __init__(self):
        self._albums = [
            AlbumConfig(
                title="Test Album",
                source="source",
                photos=None,
                cover=None
            )
        ]
        self._thumbnail = ThumbnailsConfig(height=100)
        self._output = OutputConfig(path="output")
        self._template = TemplateConfig(parameters={}, url="http://example.com/template")
        self._favicon = None
        self._docker = None
        self._title = "Test Gallery"
        self._subtitle = "Test Subtitle"
        self._data_source = LocalStorageConfig(path="source", type="local")
        self._data_storage = LocalStorageConfig(path="source", type="local")

    def with_albums(self, albums):
        self._albums = albums
        return self

    def with_thumbnail(self, thumbnail):
        self._thumbnail = thumbnail
        return self

    def with_output(self, output):
        self._output = output
        return self

    def with_template(self, template):
        self._template = template
        return self

    def with_favicon(self, favicon):
        self._favicon = favicon
        return self

    def with_docker(self, docker):
        self._docker = docker
        return self

    def with_title(self, title):
        self._title = title
        return self

    def with_subtitle(self, subtitle):
        self._subtitle = subtitle
        return self

    def with_data_source(self, data_source):
        self._data_source = data_source
        return self

    def with_data_storage(self, data_storage):
        self._data_storage = data_storage
        return self

    def build(self):
        return GalleryConfig(
            albums=self._albums,
            thumbnail=self._thumbnail,
            output=self._output,
            template=self._template,
            favicon=self._favicon,
            docker=self._docker,
            title=self._title,
            subtitle=self._subtitle,
            data_source=self._data_source,
            data_storage=self._data_storage
        )