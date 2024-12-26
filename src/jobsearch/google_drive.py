####
# Connect to Google Drive and manage the files for a service account in a folder shared.
# Check this api client for more information
# https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md
####

from enum import Enum
from typing import NewType, Self
from dataclasses import dataclass
from pathlib import Path

from googleapiclient.discovery import build
from google.oauth2 import service_account


# How to Create or get a parrent folder id?
PARENT_FOLDER_ID = "1HaijgOsMhgsH2EqWDWpxZTYz6C-ZSz71"
SERVICE_ACCOUNT_FILE = "service_token.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]


GdriveID = NewType("GdriveID", str)
GdriveName = NewType("GdriveName", str)


class SearchQueryType(Enum):
    ExactMatch = "name = '{}' and trashed = false"
    NameContaintsWithDocxEx = (
        "name contains '.docx' and name contains '{}' and trashed = false"
    )
    NameContains = "name contains '{}' and trashed = false"
    FilesInParentFolder = "'{}' in parents and trashed = false"


@dataclass
class GdriveFile:
    id: GdriveID
    name: GdriveName
    mime_type: str = None

    @property
    def extension(self) -> str:
        return f".{self.name.split('.')[1]}"

    @property
    def type(self) -> str:
        if self.is_folder():
            return "folder"
        elif self.is_document():
            return "document"
        return self.mime_type.split(".")[-1]

    def is_folder(self) -> bool:
        return self.mime_type.endswith("folder")

    def is_document(self) -> bool:
        return self.mime_type.endswith("document")

    @staticmethod
    def new(file: dict) -> Self:
        return GdriveFile(
            name=file.get("name"), id=file.get("id"), mime_type=file.get("mimeType", "")
        )

    def __repr__(self) -> str:
        return f"{self.type.upper()}: {self.name} ({self.id})"


class GoogleDrive:
    def __init__(self, parent_folder_id=PARENT_FOLDER_ID) -> None:
        self.cred = self.authenticate()
        self.service = build("drive", "v3", credentials=self.cred)
        self.parent_folder: GdriveFile = GdriveFile(
            id=parent_folder_id, name="Working Dir"
        )

    def authenticate(self):
        if not Path(SERVICE_ACCOUNT_FILE).exists():
            raise FileNotFoundError(
                f'"{SERVICE_ACCOUNT_FILE}" is not found. Please generate one from GCP.'
            )

        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        return creds

    def upload_file(self, filepath: Path) -> GdriveFile:
        file_metadata = {"name": filepath.name, "parents": [self.parent_folder.id]}
        file = (
            self.service.files()
            .create(body=file_metadata, media_body=str(filepath))
            .execute()
        )
        return GdriveFile.new(file)

    def list_files(self, folder: GdriveFile = None) -> list[GdriveFile]:
        if folder is None:
            folder = self.parent_folder

        query = SearchQueryType.FilesInParentFolder.value.format(folder.id)
        results = (
            self.service.files()
            .list(
                spaces="drive",
                q=query,
            )
            .execute()
        )
        items = results.get("files", [])
        return [GdriveFile.new(f) for f in items]

    def create_folder(self, folder_name: str, parent: str = None) -> GdriveFile:
        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent] if parent else [self.parent_folder.id],
        }
        file = self.service.files().create(body=file_metadata, fields="id").execute()
        return GdriveFile.new(file)

    def search_drive(
        self, filename: str, query_type: SearchQueryType
    ) -> list[GdriveFile]:
        """
        Search file but filter out those in the trash.
        """
        files = []
        page_token = None
        query = query_type.value.format(filename)
        while True:
            response = (
                self.service.files()
                .list(
                    q=query,
                    spaces="drive",
                    pageToken=page_token,
                )
                .execute()
            )
            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break
        files = [GdriveFile.new(f) for f in files]

        if not files:
            raise RuntimeError(f"No file or folder by the name '{filename}' was found.")
        return files

    def find_template_folder(self, template_name: str = "template") -> GdriveFile:
        files = self.search_drive(template_name, SearchQueryType.ExactMatch)
        if len(files) > 1:
            raise RuntimeError(
                "You must have only one template file in the working folder"
            )
        return files[0]

    def copy_file(
        self,
        source_file: GdriveFile,
        destination_folder: GdriveFile = None,
        new_name: str = None,
    ) -> GdriveFile:
        file_metadata = {}
        file_metadata["parents"] = [self.parent_folder.id]
        if new_name:
            file_metadata["name"] = new_name + source_file.extension
        if destination_folder:
            file_metadata["parents"] = [destination_folder.id]

        copied_file = (
            self.service.files()
            .copy(fileId=source_file.id, body=file_metadata)
            .execute()
        )
        return GdriveFile.new(copied_file)


if __name__ == "__main__":
    gd = GoogleDrive()
    # files = gd.search_drive("Salah", query_type=SearchQueryType.NameContains)
    files = gd.list_files()
    for f in files:
        print(f)
