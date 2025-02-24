from logging import Logger
import docker
import os
import shutil


class DockerImageBuilder:
    DOCKERFILE_NAME = "Dockerfile"
    NGINX_CONFIG_NAME = "nginx.conf"

    def __init__(self, docker_host: str, logger: Logger):
        self.docker_host = docker_host
        self.logger = logger

    def build_docker_image(self, image_name: str, image_version: str, gallery_output_path: str):
        if not self.check_if_docker_is_running():
            raise Exception("Docker engine is not running")

        shutil.copy(
            os.path.join(os.path.dirname(__file__), self.DOCKERFILE_NAME),
            os.path.join(gallery_output_path, self.DOCKERFILE_NAME),
        )

        shutil.copy(
            os.path.join(os.path.dirname(__file__), self.NGINX_CONFIG_NAME),
            os.path.join(gallery_output_path, self.NGINX_CONFIG_NAME),
        )

        client = self.__create_client()

        self.logger.info(f"Building image {image_name}:{image_version}")
        image, _ = client.images.build(path=gallery_output_path, tag=f"{image_name}:{image_version}", nocache=True)
        self.logger.info(f"Image {image.short_id} built successfully")

    def check_if_docker_is_running(self):
        try:
            client = self.__create_client()
            client.ping()
            return True
        except Exception:
            return False

    def __create_client(self) -> docker.DockerClient:
        client = docker.DockerClient(base_url=self.docker_host, timeout=10)
        return client


if __name__ == "__main__":
    logger = Logger("Docker")
    DockerImageBuilder("tcp://localhost:2375", logger).build_docker_image("ggallery", "latest", "docs")
