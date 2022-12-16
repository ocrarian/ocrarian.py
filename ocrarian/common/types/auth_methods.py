"""Google Drive API authentication methods"""
from enum import Enum, auto


class AuthenticationMethods(Enum):
    """ Google Drive API authentication methods enum """
    SERVICE_ACCOUNT = auto()
    CLIENT_SECRET = auto()
