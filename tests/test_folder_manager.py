import shutil
from pathlib import Path
from jobsearch.folder_manager import LocalFolder

import pytest


@pytest.fixture()
def test_dir():
    test_dir = Path.home() / "test"
    test_dir.mkdir()
    yield test_dir
    shutil.rmtree(test_dir)


def test_local_folder(test_dir):
    lf = LocalFolder(working_folder=test_dir)

    lf.create_folder("20241225_data_engineer")

    assert len(list(test_dir.glob("*"))) == 1
