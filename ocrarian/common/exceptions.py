"""ocrarian custom exceptions"""


class MissingClientSecretsFile(Exception):
    """Exception raised when client_secret.json is missing"""
    def __init__(self, missing_file, user_config_dir):
        super().__init__(self)
        self.missing_file = missing_file
        self.user_config_dir = user_config_dir

    def __str__(self):
        return f"{self.missing_file} is missing! " \
               f"Please follow the instructions in order to create and download it, " \
               f"then copy it to app config directory {self.user_config_dir} as explained."
