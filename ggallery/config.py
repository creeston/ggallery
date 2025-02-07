import os
from .model import GalleryConfig
import yaml
import re


def load_env_variable_and_escape_slash(value: str) -> str:
    variable_value = os.environ[value]
    variable_value = variable_value.replace("\\", "\\\\")  # escape backslashes
    return variable_value


def load_config(config_path: str) -> GalleryConfig:
    with open(config_path, "r") as f:
        content = f.read()
        try:
            content = re.sub(r"\$\{(\w+)\}", lambda match: load_env_variable_and_escape_slash(match.group(1)), content)
        except KeyError as e:
            print(f"Environment variable {e} not found")
            raise e

        obj = yaml.safe_load(content)
        return GalleryConfig(**obj)
