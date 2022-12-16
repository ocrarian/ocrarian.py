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


class IncorrectExportFormat(Exception):
    """Exception raised when an incorrect export format is configured."""

    def __init__(self, incorrect_export_format, available_formats):
        super().__init__(self)
        self.incorrect_export_format = incorrect_export_format
        self.available_formats = available_formats

    def __str__(self):
        return f"{self.incorrect_export_format} is an incorrect export format! " \
               f"export_format must be one of {self.available_formats}"


class IncorrectAuthMethod(Exception):
    """Exception raised when an incorrect authentication method is configured."""

    def __init__(self, incorrect_auth_method, available_methods):
        super().__init__(self)
        self.incorrect_auth_method = incorrect_auth_method
        self.available_methods = available_methods

    def __str__(self):
        return f"{self.incorrect_auth_method} is an incorrect authentication method! " \
               f"authentication must be one of {self.available_methods}"


class FileNotFound(Exception):
    """Exception raised when file type cannot be determined."""

    def __init__(self, file):
        super().__init__(self)
        self.file = file

    def __str__(self):
        return f"File {self.file} does not exist!"


class UnknownFileType(Exception):
    """Exception raised when file type cannot be determined."""

    def __init__(self, file):
        super().__init__(self)
        self.file = file

    def __str__(self):
        return f"Cannot determine file {self.file} type! " \
               f"Please make sure that the file you are trying to use is valid and try again."


class UnsupportedFile(Exception):
    """Exception raised when an incorrect export format is configured."""

    def __init__(self, file_extension, file_mime_type, supported_types):
        super().__init__(self)
        self.file_extension = file_extension
        self.file_mime_type = file_mime_type
        self.supported_types = supported_types

    def __str__(self):
        return f"{self.file_extension} ({self.file_mime_type}) is an unsupported file type! " \
               f"input file type must be one of {self.supported_types}"
