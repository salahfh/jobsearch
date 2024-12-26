from abc import ABC, abstractmethod
from pathlib import Path


class FolderManager(ABC):
    def __init__(self, working_folder: Path) -> None:
        self.working_folder = working_folder

    @abstractmethod
    def get_file(self):
        pass

    @abstractmethod
    def create_folder(self, folder_name: str) -> Path:
        pass

    def set_template_folder(self, folder_path: Path) -> None:
        self.template_folder = folder_path

    def copy_templates(self, new_dir: Path):
        pass


class LocalFolder(FolderManager):
    def get_file(self):
        return self.working_folder.glob("*")

    def create_folder(self, folder_name: str) -> Path:
        dir = self.working_folder / folder_name
        dir.mkdir(exist_ok=True, parents=True)
        return dir


class GoogleDrive(FolderManager):
    # Check this api client for more information
    # https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md
    pass