from enum import Enum


class Types(Enum):
    """ Google Docs export allowed types
    https://developers.google.com/drive/api/v3/ref-export-formats
    """
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ODT = "application/vnd.oasis.opendocument.text"
    RTF = "application/rtf"
    PDF = "application/pdf"
    TXT = "text/plain"
    HTML = "application/zip"  # Zipped HTML
    EPUB = "application/epub+zip"
