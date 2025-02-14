import importlib.util
import os
from pathlib import Path
import sys
import tempfile

from .base_renderer import BaseRenderer
import requests
from zipfile import ZipFile
from io import BytesIO


class RendererImporter:
    def __init__(self, template_module_url: str):
        if not template_module_url.startswith("https://github.com/"):
            raise ValueError("URL must be a GitHub repository")
        self.template_module_url = template_module_url

    def __enter__(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = Path(self.temp_dir.name)

        response = requests.get(f"{self.template_module_url}/archive/refs/heads/main.zip")
        if response.status_code != 200:
            raise ValueError("Failed to download repository")

        with ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall(self.temp_dir_path)

        repo_name = os.path.basename(self.template_module_url)
        extracted_dir = os.path.join(self.temp_dir_path, f"{repo_name}-main")
        instance = self.__find_renderer_implementation(extracted_dir)

        if instance is None:
            raise ValueError("No renderer found")

        return instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_dir is not None:
            self.temp_dir.cleanup()

    def __find_renderer_implementation(self, module_dir: str) -> BaseRenderer | None:
        sys.path.insert(0, module_dir)
        instance: BaseRenderer | None = None
        module_directory = None
        for root, _, files in os.walk(module_dir):
            for file in files:
                if instance is not None:
                    break
                if file.endswith(".py"):
                    module_name = os.path.splitext(file)[0]
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(root, file))
                    if spec is None:
                        continue
                    module = importlib.util.module_from_spec(spec)
                    if spec.loader is None:
                        continue
                    spec.loader.exec_module(module)
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, BaseRenderer) and attr is not BaseRenderer:
                            instance = attr()
                            break
        sys.path.pop(0)
        return instance
