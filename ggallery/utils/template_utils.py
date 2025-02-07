from jinja2 import Environment, PackageLoader

from ..model import AlbumConfig


def render_template(albums: list[AlbumConfig], base_url: str, title: str, subtitle: str | None):
    env = Environment(loader=PackageLoader("ggallery", "templates"))
    template = env.get_template("index.html.j2")

    items = []
    album_id = 1
    for album in albums:
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
                    "title": None,
                    "id": None,
                }
            )
        album_id += 1

    return template.render(
        items=items,
        items_base_url=base_url,
        title=title,
        subtitle=subtitle,
        albums=albums,
    )
