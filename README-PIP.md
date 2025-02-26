<div align="center">
  <h1 align="center">ggallery</h1>
</div>


[![npm](https://img.shields.io/badge/demo-online-008000.svg)](https://creeston.github.io/ggallery)

`ggallery` is a Python tool that generates a static HTML photo gallery website from a YAML specification and from given renderer plugin. It allows you to create beautiful and customizable photo galleries with ease, using various data sources and storage providers.

## Features

- **Static HTML Generation using plugins**: Create a static HTML photo gallery that can be hosted on any web server, using a custom renderer plugin.
- **Multiple Data Sources**: Supports local file system and Azure Blob Storage as data sources.
- **Thumbnail Generation**: Automatically generate thumbnails for your images.
- **Docker image creation**: Create a Docker image (using nginx) with the generated gallery.

## Available Renderer Plugins

- https://github.com/creeston/ggallery-nanogallery2 - template built on top of nanogallery2 and bulma css framework. [Live Demo](https://creeston.github.io/ggallery-nanogallery2/)

## Usage

To install `ggallery`, you need to have Python with pip package manager in your system. 
Then you can install the tool using the following command:

```sh
pip install ggallery
```

You can run the `ggallery` using the following commands:

```sh
python -m ggallery -f /path/to/your/gallery.yaml
```

or

```sh
ggallery -f /path/to/your/gallery.yaml
```

If you have the `gallery.yaml` file in the current directory, you can run the tool without specifying the file path:

```sh
ggallery
```

## Gallery Specification Examples

### Local Gallery with Docker Image

Photos and HTML files are stored in the same directory as the static website. It will procude a directory ready to be served by a web server.

1. Set environment variables (or create .env file)

- `LOCAL_PHOTOS_PATH`: Path to the directory containing photos.
- `DOCKER_HOST` Hostname of the Docker host. (e.g tcp://localhost:2375)

2. Create a `gallery.yaml` file with the following content:

```yaml
title: Local Gallery
subtitle: Gallery with photos stored in the same directory as static website.

thumbnail:
    height: 400

template:
    url: https://github.com/creeston/ggallery-nanogallery2

data_source:
    type: local
    path: "${LOCAL_PHOTOS_PATH}" # Path to the directory containing photos.

data_storage:
    type: local # Store photos in the same directory as the static website.

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

# Output directory for the generated gallery website.
output:
    path: docs
    index: index.html

# Docker image configuration
docker:
    image_name: "username/my-photo-gallery"
    image_version: "latest"
    host: "${DOCKER_HOST}"
```

### Azure Blob Storage Example

Photos are stored in Azure Blob Storage. The generated gallery will contain links to the photos stored in Azure Blob Storage.

1. Set environment variables (or create .env file)

- `LOCAL_PHOTOS_PATH`: Path to the directory containing photos.
- `AZURE_CONTAINER`: Azure Blob Storage container name.
- `AZURE_CONNECTION_STRING`: Azure Blob Storage connection string.

2. Create a `gallery.yaml` file with the following content:

```yaml
title: Azure Gallery
subtitle: Gallery of photos stored in Azure Blob Storage

favicon:
    type: fontawesome
    name: camera-retro

thumbnail:
    height: 400

template:
    url: https://github.com/creeston/ggallery-nanogallery2

data_source:
    type: local
    path: "${LOCAL_PHOTOS_PATH}"

# Azure Blob Storage configuration, used to store photos and thumbnails.
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
    index: index.html
```

## Implementing a Custom Template

ggallery doesn't contain any templates by default. You can create your own plugin by implementing `ggalllery.renderers.BaseRenderer` class. The plugin can be stored either locally or in a public github repository. URL to the repository should be provided in the `gallery.yaml` file in the `template.url` field.


Examples:
- https://github.com/creeston/ggallery-nanogallery2


## Contribution

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request on the [GitHub repository](https://github.com/creeston/ggallery).


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.