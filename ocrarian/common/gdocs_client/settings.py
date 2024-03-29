"""ocrarian config"""
from configparser import ConfigParser

from ocrarian.common.gdocs_client.exceptions import MissingClientSecretsFile, IncorrectExportFormat, IncorrectAuthMethod
from ocrarian.common.types.auth_methods import AuthenticationMethods
from ocrarian.common.types.export_types import ExportTypes


class Settings:
    """Config class for ocrarian
    This class is responsible for creating configuration directory and settings file.
    It also handles settings load, save and delete."""

    def __init__(self, storage_config):
        self.storage_config = storage_config
        self.check_client_secret()
        self.export_format = None
        self.authentication_method = None
        self._config_path = self.check_config()
        if self._config_path:
            self._config = self.load_config()
        else:
            self._config = self.create_config()
        self.review_config()

    def check_client_secret(self):
        """Check that client_secret.json is available in user_config_dir."""
        if not (self.storage_config.user_config_dir / "client_secret.json").exists():
            raise MissingClientSecretsFile(
                "client_secret.json", self.storage_config.user_config_dir)

    def check_config(self):
        """Check that config.ini is available in user_config_dir."""
        return bool((self.storage_config.user_config_dir / "config.ini").exists())

    def load_config(self):
        """Load configuration from user_config_dir."""
        config = ConfigParser()
        config.read(self.storage_config.user_config_dir / "config.ini")
        return config

    def create_config(self):
        """Create configuration with defaults for first time run."""
        new_config = ConfigParser()
        new_config['settings'] = {}
        new_config['settings']['export_format'] = 'TXT'
        new_config['settings']['authentication'] = 'SERVICE_ACCOUNT'
        self.save_config(new_config)
        return new_config

    def save_config(self, new_config=None):
        """Save configuration to user_config_dir."""
        with open(self.storage_config.user_config_dir / "config.ini", "w") as config_file:
            if new_config:
                new_config.write(config_file)
            else:
                self._config.write(config_file)

    def review_config(self):
        """Ensure that configuration is valid."""
        # export_format
        chosen_export_format = self._config['settings']['export_format']
        if not any([chosen_export_format == i.name for i in ExportTypes]):
            raise IncorrectExportFormat(chosen_export_format, [i.name for i in ExportTypes])
        self.export_format = chosen_export_format
        chosen_authentication_method = self._config['settings']['authentication']
        if not any([chosen_authentication_method == i.name for i in AuthenticationMethods]):
            raise IncorrectAuthMethod(chosen_authentication_method, [i.name for i in AuthenticationMethods])
        self.authentication_method = chosen_authentication_method

    def __getitem__(self, name):
        """Get the value of a setting."""
        return self._config[name]

    def __setitem__(self, name, value):
        """Set the value of a setting."""
        self._config[name] = value

    def __delitem__(self, name):
        """Remove a setting."""
        self._config.pop(name)
