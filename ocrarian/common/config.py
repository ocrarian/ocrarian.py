"""ocrarian config"""
from pathlib import Path
from configparser import ConfigParser
from appdirs import AppDirs

from ocrarian import APP_NAME
from ocrarian.common.exceptions import MissingClientSecretsFile, IncorrectExportFormat
from ocrarian.common.export_types import Types


class Config(AppDirs):
    """Config class for ocrarian
    This class is responsible for creating configuration directory and settings file.
    It also handles settings load, save and delete."""

    def __init__(self):
        super().__init__(appname=APP_NAME)
        self.user_docs_dir = Path("~/Documents").expanduser()
        self.create_directories()
        self.check_client_secret()
        self._config_path = self.check_config()
        if self._config_path:
            self._config = self.load_config()
        else:
            self._config = self.create_config()
        self.review_config()

    def create_directories(self):
        """Create config and docs directories."""
        # pylint: disable=no-member
        # Instance of 'user_config_dir' has no 'exists' member (no-member)
        # Instance of 'user_config_dir' has no 'mkdir' member (no-member)
        if not self.user_config_dir.exists():
            self.user_config_dir.mkdir()
        if not self.user_docs_dir.exists():
            self.user_docs_dir.mkdir()

    def check_client_secret(self):
        """Check that client_secret.json is available in user_config_dir."""
        if not (self.user_config_dir / "client_secret.json").exists():
            raise MissingClientSecretsFile("client_secret.json", self.user_config_dir)

    def check_config(self):
        """Check that config.ini is available in user_config_dir."""
        return bool((self.user_config_dir / "config.ini").exists())

    def load_config(self):
        """Load configuration from user_config_dir."""
        config = ConfigParser()
        config.read(self.user_config_dir / "config.ini")
        return config

    def create_config(self):
        """Create configuration with defaults for first time run."""
        new_config = ConfigParser()
        new_config['settings'] = {}
        new_config['settings']['export_format'] = 'TXT'
        self.save_config(new_config)
        return new_config

    def save_config(self, new_config=None):
        """Save configuration to user_config_dir."""
        with open(self.user_config_dir / "config.ini", "w") as config_file:
            if new_config:
                new_config.write(config_file)
            else:
                self._config.write(config_file)

    def review_config(self):
        """Ensure that configuration is valid."""
        # export_format
        chosen_export_format = self._config['settings']['export_format']
        vaild_export_format = [i for i in Types if i.name == chosen_export_format]
        if not vaild_export_format:
            raise IncorrectExportFormat(chosen_export_format, [i.name for i in Types])

    def __getitem__(self, name):
        """Get the value of a setting."""
        return self._config[name]

    def __setitem__(self, name, value):
        """Set the value of a setting."""
        self._config[name] = value

    def __delitem__(self, name):
        """Remove a setting."""
        self._config.pop(name)
