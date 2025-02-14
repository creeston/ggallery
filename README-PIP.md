<div align="center">
  <h1 align="center">ggallery</h1>
</div>


[![npm](https://img.shields.io/badge/demo-online-008000.svg)](https://creeston.github.io/ggallery)

`ggallery` is a Python tool that generates a static HTML photo gallery website from a YAML specification and from given renderer plugin. It allows you to create beautiful and customizable photo galleries with ease, using various data sources and storage providers.

## Features

- **Static HTML Generation using plugins**: Create a static HTML photo gallery that can be hosted on any web server, using a custom renderer plugin.
- **Multiple Data Sources**: Supports local file system and Azure Blob Storage as data sources.
- **Thumbnail Generation**: Automatically generate thumbnails for your images.

## Available Renderer Plugins

- https://github.com/creeston/ggallery-nanogallery2 - template built on top of nanogallery2 and bulma css framework.

## Usage

To use `ggallery`, you need to have Python installed.

```sh
pip install ggallery
```

You can run the tool using the following commands:

```sh
python -m ggallery -f /path/to/your/gallery.yaml
```

or

```sh
ggallery -f /path/to/your/gallery.yaml
```

## Examples

### Local Gallery Example

Create a `gallery.yaml` file with the following content:

```yaml
title: Local Gallery
subtitle: Gallery with photos stored in the same directory as static website.

thumbnail:
    height: 400

template:
    url: https://github.com/creeston/ggallery-nanogallery2

data_source:
    type: local
    path: "${LOCAL_PHOTOS_PATH}"

data_storage:
    type: local

albums:
    - title: "Japan"
      subtitle: "Photos from my trip to Japan"
      source: "japan"
      cover: "view on the Fuji.jpg"

    - title: "Italy"
      source: "italy"
      cover: "colliseum.jpg"
      photos:
          - title: "View at the Colosseum at night"
            source: "colliseum.jpg"

output:
    path: docs
```

Set the `LOCAL_PHOTOS_PATH` environment variable to the path where your photos are stored.

Run the tool:

```sh
python -m ggallery gallery.yaml
```

### Azure Blob Storage Example

Create a `gallery.yaml` file with the following content:

```yaml
title: Azure Gallery
subtitle: Gallery of photos stored in Azure Blob Storage

favicon:
    type: fontawesome
    name: camera-retro

thumbnail:
    height: 400

template:
    name: "nano-gallery"

data_source:
    type: local
    path: "${LOCAL_PHOTOS_PATH}"

data_storage:
    type: azure-blob
    container: "${AZURE_CONTAINER}"
    connection_string: "${AZURE_CONNECTION_STRING}"

albums:
    - title: "Japan"
      subtitle: "Photos from my trip to Japan"
      source: "japan"
      cover: "view on the Fuji.jpg"

    - title: "Italy"
      source: "italy"
      cover: "colliseum.jpg"
      photos:
          - title: "View at the Colosseum at night"
            source: "colliseum.jpg"

output:
    path: docs
```

Set the `LOCAL_PHOTOS_PATH`, `AZURE_CONTAINER`, and `AZURE_CONNECTION_STRING` environment variables.

Run the tool:

```sh
python -m ggallery gallery.yaml
```

## Contribution

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request on the [GitHub repository](https://github.com/creeston/ggallery).


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.