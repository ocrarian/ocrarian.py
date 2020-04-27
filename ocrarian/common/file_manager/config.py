"""ocrarian file manager config"""
from pathlib import Path
from appdirs import AppDirs

from ocrarian import APP_NAME


class Config(AppDirs):
    """Config class for ocrarian
    This class is responsible for creating configuration directory and settings file.
    It also handles settings load, save and delete."""

    def __init__(self):
        super().__init__(appname=APP_NAME)
        self.user_docs_dir = Path("~/Documents").expanduser()
        self.create_directories()

    def create_directories(self):
        """Create config and docs directories."""
        # pylint: disable=no-member
        # Instance of 'user_config_dir' has no 'exists' member (no-member)
        # Instance of 'user_config_dir' has no 'mkdir' member (no-member)
        if not self.user_config_dir.exists():
            self.user_config_dir.mkdir()
        if not self.user_docs_dir.exists():
            self.user_docs_dir.mkdir()
        if not self.user_cache_dir.exists():
            self.user_cache_dir.mkdir()
