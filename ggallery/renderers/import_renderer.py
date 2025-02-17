import fnmatch
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
        if template_module_url.startswith("http://") or template_module_url.startswith("https://"):
            if not self.__is_github_repository(template_module_url):
                raise ValueError("URL must be a GitHub repository")
        self.template_module_url = template_module_url

    def __enter__(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = Path(self.temp_dir.name)

        if self.__is_github_repository(self.template_module_url):
            plugin_dir = self.__download_github_repo()
        else:
            plugin_dir = self.template_module_url

        instance = self.__find_renderer_implementation(plugin_dir)
        if instance is None:
            raise ValueError("No renderer found")

        return instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_dir is not None:
            self.temp_dir.cleanup()

    def __is_github_repository(self, url: str) -> bool:
        return url.startswith("https://github.com/")

    def __copy_plugin(self) -> str:
        plugin_name = os.path.basename(self.template_module_url)
        dest_dir = os.path.join(self.temp_dir_path, plugin_name)
        os.makedirs(dest_dir, exist_ok=True)
        for root, _, files in os.walk(self.template_module_url):
            for file in files:
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_dir, file)
                with open(src_path, "rb") as src_file, open(dest_path, "wb") as dest_file:
                    dest_file.write(src_file.read())
        return dest_dir

    def __download_github_repo(self) -> str:
        repo_name = os.path.basename(self.template_module_url)
        response = requests.get(f"https://api.github.com/repos/{repo_name}/zipball")
        if response.status_code != 200:
            raise ValueError("Failed to download repository")
        with ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall(self.temp_dir_path)

        repo_name = os.path.basename(self.template_module_url)
        extracted_dir = os.path.join(self.temp_dir_path, f"{repo_name}-main")
        return extracted_dir

    def __find_renderer_implementation(self, module_dir: str) -> BaseRenderer | None:
        sys.path.insert(0, module_dir)
        instance: BaseRenderer | None = None
        gitignore_path = os.path.join(module_dir, ".gitignore")
        if os.path.exists(gitignore_path):
            gitignore_content = Path(gitignore_path).read_text()
            files_to_ignore = gitignore_content.split("\n")
        else:
            files_to_ignore = []
        for root, _, files in os.walk(module_dir, topdown=False):
            rel_path = os.path.relpath(root, module_dir)
            if rel_path.startswith("."):  # Ignore hidden directories
                continue

            if os.path.dirname(rel_path) in files_to_ignore:  # Ignore directories listed in .gitignore
                continue

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
