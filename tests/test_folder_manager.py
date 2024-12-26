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
    lf = LocalFolder(working_folder=test_dir, template_folder="")

    lf.create_folder("20241225_data_engineer")

    assert len(list(test_dir.glob("*"))) == 1


def test_local_folder_copy_template(test_dir):
    template_folder = test_dir / "template_folder"
    template_folder.mkdir(exist_ok=True)
    template = template_folder / "template.docx"
    template.touch()
    new_dirname = test_dir / Path("20241225_data_engineer")

    lf = LocalFolder(working_folder=test_dir, template_folder=template_folder)
    lf.copy_templates_to(new_dirname)

    assert new_dirname.resolve() in [f for f in test_dir.glob("*")]
    assert len(list(new_dirname.glob("*.docx"))) == 1
