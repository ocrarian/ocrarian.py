"""ocrarian supported input file types"""
from enum import Enum


class SupportedTypes(Enum):
    """input allowed files types"""
    PDF = "application/pdf"
    JPG = "image/jpeg"
    PNG = "image/png"
