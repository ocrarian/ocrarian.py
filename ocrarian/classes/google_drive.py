"""Google Drive client implementation"""
import pickle
from io import FileIO
from pathlib import Path

from ocrarian import WORK_DIR

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


class GdriveClient:
    """Google Drive client"""

    def __init__(self):
        self._token_file = Path(f"{WORK_DIR}/token.pickle")
        self._oath_scope = ["https://www.googleapis.com/auth/drive"]
        self._service = self.authenticate()

    def load_token(self):
        """load google drive oauth token"""
        with open(self._token_file, 'rb') as out:
            return pickle.load(out)

    def save_token(self, credentials):
        """save google drive oauth token"""
        with open(self._token_file, 'wb') as token:
            pickle.dump(credentials, token)

    def authenticate(self):
        """authenticate google drive using oauth or refresh token"""
        if self._token_file.exists():
            credentials = self.load_token()
            if credentials is None or not credentials.valid:
                if credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(f'{WORK_DIR}/client_secret.json', self._oath_scope)
            credentials = flow.run_console(port=0)
        self.save_token(credentials)
        return build('drive', 'v3', credentials=credentials, cache_discovery=False)

    def ocr(self, file_path: Path):
        """upload a file to Google Drive then export the uploaded file to a text file"""
        mime_type = 'application/vnd.google-apps.document'
        file_metadata = {'name': file_path.name, 'mimeType': mime_type}
        media_body = MediaFileUpload(file_path, mimetype=mime_type,
                                     resumable=True, chunksize=50 * 1024 * 1024)
        file = self._service.files().create(body=file_metadata, media_body=media_body)
        uploaded = None
        while uploaded is None:
            _, uploaded = file.next_chunk()
        # Convert to text
        txt_file = Path(f"{file_path.stem}.txt")
        download = MediaIoBaseDownload(
            FileIO(f"{WORK_DIR}/{txt_file.name}", 'wb'),
            self._service.files().export_media(fileId=uploaded['id'], mimeType="text/plain")
        )
        downloaded, status = False, False
        while downloaded is False:
            status, downloaded = download.next_chunk()
        if status:
            self._service.files().delete(fileId=uploaded["id"]).execute()
            return txt_file