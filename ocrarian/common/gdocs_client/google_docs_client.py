"""Google Docs client implementation"""
import pickle
from io import FileIO
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from ocrarian.common.gdocs_client.settings import Settings
from ocrarian.common.types.auth_methods import AuthenticationMethods
from ocrarian.common.types.export_types import ExportTypes


class GDocsClient:
    """Google Drive client"""

    def __init__(self, config: Settings):
        self.settings = config
        self._token_file = Path(f"{self.settings.storage_config.user_config_dir}/token.pickle")
        self._oauth_scope = ["https://www.googleapis.com/auth/drive"]
        self._service = self.authenticate(
            use_service_account=self.settings.authentication_method == AuthenticationMethods.SERVICE_ACCOUNT.name
        )

    def load_token(self):
        """load google drive oauth token"""
        with open(self._token_file, 'rb') as out:
            return pickle.load(out)

    def save_token(self, credentials):
        """save google drive oauth token"""
        with open(self._token_file, 'wb') as token:
            pickle.dump(credentials, token)

    def authenticate(self, use_service_account=False):
        """authenticate Google Drive using oauth or refresh token"""
        if use_service_account:
            credentials = ServiceAccountCredentials.from_service_account_file(
                f'{self.settings.storage_config.user_config_dir}/service_account.json'
            )
        else:
            if self._token_file.exists():
                credentials = self.refresh_token()
            else:
                credentials = self.create_token()
            self.save_token(credentials)
        return build('drive', 'v3', credentials=credentials, cache_discovery=False)

    def refresh_token(self):
        """refresh google drive oauth token"""
        credentials = self.load_token()
        if credentials is None or not credentials.valid:
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
        return credentials

    def create_token(self):
        """authorize google drive for the first time"""
        flow = InstalledAppFlow.from_client_secrets_file(
            f'{self.settings.storage_config.user_config_dir}/client_secret.json', self._oauth_scope)
        credentials = flow.run_local_server(port=0)
        return credentials

    def ocr(self, file_path: Path):
        """upload a file to Google Drive then export the uploaded file to a text file"""
        # pylint: disable=no-member
        # Instance of 'Resource' has no 'files' member (no-member)
        mime_type = 'application/vnd.google-apps.document'
        file_metadata = {'name': file_path.name, 'mimeType': mime_type}
        media_body = MediaFileUpload(file_path, mimetype=mime_type,
                                     resumable=True, chunksize=5 * 1024 * 1024)
        file = self._service.files().create(body=file_metadata, media_body=media_body)
        uploaded = None
        while uploaded is None:
            _, uploaded = file.next_chunk()
        # Convert to text
        txt_file = Path(f"{self.settings.storage_config.user_cache_dir}/{file_path.stem}.txt").absolute()
        download = MediaIoBaseDownload(
            FileIO(txt_file, 'wb'),
            self._service.files().export_media(
                fileId=uploaded['id'],
                mimeType=ExportTypes[self.settings['settings']['export_format']].value)
        )
        downloaded, status = False, False
        while downloaded is False:
            status, downloaded = download.next_chunk()
        if status:
            self._service.files().delete(fileId=uploaded["id"]).execute()
            return txt_file
