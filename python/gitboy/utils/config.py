"""
Function to handle config while using Gitboy.

Config is expected to be a JSON file located at GITBOY_CONFIG_PATH (default: $HOME/.config/gitboy/config.json),
with the following structure:
    {
        "token": "<Github API token>",
        "organization": "<organization name>"
    }
"""
import os
import json


CONFIG_PATH = os.environ.get("GITBOY_CONFIG_PATH", os.path.join(os.environ["HOME"], ".config/gitboy/config.json"))

if not os.path.isfile(CONFIG_PATH):
    raise RuntimeError(f"Could not find config! Check if a gitboy config JSON file exists at: {CONFIG_PATH}")


class Config:
    def __init__(self, config_path: str):
        self.config_path = config_path

        if not os.path.isfile(self.config_path):
            raise RuntimeError(
                f"Could not find config! Check if a gitboy config JSON file exists at: {self.config_path}"
            )

        self._config = None
        self.token = None
        self.organization = None

        self.load_config()

    def load_config(self):
        with open(self.config_path) as f:
            self._config = json.load(f)

        self.token = self._config.get("token")
        if self.token is None:
            raise RuntimeError("Github API token has not been specified in the config.")

        self.organization = self._config.get("organization")


CONFIG = Config(CONFIG_PATH)


def get_config() -> CONFIG:
    return CONFIG


def reload_config() -> CONFIG:
    CONFIG.load_config()
    return get_config()
