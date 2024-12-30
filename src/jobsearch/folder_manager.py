import shutil
from typing import Any
from abc import ABC, abstractmethod
from pathlib import Path

from jobsearch.google_drive import GoogleDrive, GdriveFile


class FolderManager(ABC):
    def __init__(self, working_folder: Path, template_folder: str) -> None:
        self.working_folder = working_folder
        self.template_folder = template_folder

    @abstractmethod
    def get_files(self) -> list[Any]:
        pass

    @abstractmethod
    def create_folder(self, folder_name: str) -> Path:
        pass

    @abstractmethod
    def copy_templates_to(
        self,
        new_dir: Any,
    ):
        pass


class LocalFolder(FolderManager):
    def get_files(self) -> list[Path]:
        return self.working_folder.glob("*")

    def create_folder(self, folder_name: str) -> Path:
        dir = self.working_folder / folder_name
        dir.mkdir(exist_ok=True, parents=True)
        return dir

    def copy_templates_to(self, new_dir: Path):
        self.create_folder(new_dir)
        for f in self.template_folder.glob("*"):
            shutil.copy(f, new_dir)


class CloudFolder(FolderManager):
    def __init__(self, template_folder):
        super().__init__(working_folder='', template_folder=template_folder)
        self.provider = GoogleDrive()

    def get_files(self) -> list[GdriveFile]:
        files = []
        for f in self.provider.list_files():
            if not f.is_folder():
                files.append(f)
        return files

    def create_folder(self, folder_name: str) -> GdriveFile:
        return self.provider.create_folder(folder_name)

    def copy_templates_to(self, new_dir: str):
        template_dir = self.provider.find_template_folder(
            template_name=self.template_folder
        )
        destination = self.provider.create_folder(new_dir)
        for f in self.provider.list_files(template_dir):
            self.provider.copy_file(f, destination)


if __name__ == "__main__":
    cf = CloudFolder(template_folder="0000-00-00 Template_Folder")
    cf.copy_templates_to("20251229_Data_Engineer")
