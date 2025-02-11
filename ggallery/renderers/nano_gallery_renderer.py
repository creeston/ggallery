from jinja2 import Environment, PackageLoader
from .base_renderer import BaseRenderer
from ..model import RendererParameters


class NanoGalleryTemplateRenderer(BaseRenderer):
    def render(
        self,
        parameters: RendererParameters,
    ) -> str:
        env = Environment(loader=PackageLoader("ggallery", "templates"))
        template = env.get_template("nano-gallery.html.j2")

        items = []
        album_id = 1
        for album in parameters.albums:
            album.id = album_id
            photos = album.photos
            if not photos:
                continue

            album_cover = photos[0].thumbnail if album.cover is None else album.cover
            items.append(
                {
                    "src": album_cover,
                    "srct": None,
                    "album_id": None,
                    "kind": "album",
                    "title": album.title,
                    "id": album_id,
                }
            )

            for photo in photos:
                items.append(
                    {
                        "src": photo.filename,
                        "srct": photo.thumbnail,
                        "album_id": album_id,
                        "kind": None,
                        "title": photo.title,
                        "id": None,
                    }
                )
            album_id += 1

        return template.render(
            items=items,
            items_base_url=parameters.base_url,
            title=parameters.title,
            subtitle=parameters.subtitle,
            favicon=parameters.favicon,
            albums=parameters.albums,
            thumbnail_height=parameters.thumbnail_height,
        )
