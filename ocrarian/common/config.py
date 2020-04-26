from pathlib import Path
from configparser import ConfigParser
from appdirs import AppDirs

from ocrarian import app_name
from ocrarian.common.exceptions import MissingClientSecretsFile


class Config(AppDirs):
    def __init__(self):
        super().__init__(appname=app_name)
        self.user_docs_dir = Path("~/Documents").expanduser()
        self.create_directories()
        self.check_client_secret()
        self._config_path = self.check_config()
        if self._config_path:
            self._config = self.load_config()
        else:
            self._config = self.create_config()

    def create_directories(self):
        if not self.user_config_dir.exists():
            self.user_config_dir.mkdir()
        if not self.user_docs_dir.exists():
            self.user_docs_dir.mkdir()

    def check_client_secret(self):
        if not (self.user_config_dir / "client_secret.json").exists():
            raise MissingClientSecretsFile("client_secret.json", self.user_config_dir)

    def check_config(self):
        return bool((self.user_config_dir / "config.ini").exists())

    def load_config(self):
        config = ConfigParser()
        config.read(self.user_config_dir / "config.ini")
        return config

    def create_config(self):
        new_config = ConfigParser()
        new_config['settings'] = {}
        new_config['settings']['export_format'] = 'TXT'
        self.save_config(new_config)
        return new_config

    def save_config(self, new_config=None):
        with open(self.user_config_dir / "config.ini", "w") as config_file:
            if new_config:
                new_config.write(config_file)
            else:
                self._config.write(config_file)

    def __getitem__(self, name):
        """Get the value of a setting."""
        return self._config[name]

    def __setitem__(self, name, value):
        """Set the value of a setting."""
        self._config[name] = value

    def __delitem__(self, name):
        """Remove a setting."""
        self._config.pop(name)
