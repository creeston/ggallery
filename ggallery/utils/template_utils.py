from jinja2 import Environment, PackageLoader


def render_template(albums, base_url: str, title: str, subtitle: str):
    env = Environment(loader=PackageLoader("ggallery", "templates"))
    template = env.get_template("index.html.j2")

    items = []
    for album in albums:
        images = album["images"]
        album_id = album["id"]
        items.append(
            {
                "src": images[0][1],
                "srct": None,
                "album_id": None,
                "kind": "album",
                "title": album["title"],
                "id": album_id,
            }
        )

        for image, thumbnail in images:
            items.append(
                {
                    "src": image,
                    "srct": thumbnail,
                    "album_id": album_id,
                    "kind": None,
                    "title": None,
                    "id": None,
                }
            )

    return template.render(
        items=items,
        items_base_url=base_url,
        title=title,
        subtitle=subtitle,
        albums=albums,
    )
