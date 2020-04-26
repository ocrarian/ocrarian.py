"""ocrarian file manager exceptions"""


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
