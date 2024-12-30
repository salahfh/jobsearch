import json
import shutil
from pathlib import Path
from jobsearch.storage.repo import FileRepository, DataIntegrityException

import pytest


@pytest.fixture()
def test_dir():
    test_dir = Path.home() / "test"
    test_dir.mkdir()
    yield test_dir
    shutil.rmtree(test_dir)


def test_write_file_repo(test_dir):
    file = test_dir / "data.json"
    repo = FileRepository(connection={'filepath': file, 'key': 'url'})

    data = {"url": "1234.com", 'fields': "something"}
    _ = repo.write(data)

    with open(file) as f:
        written_data = json.loads(f.readlines()[0])

    assert written_data.get('url') == data.get('url')
    assert written_data.get('id', None) is not None

def test_get_id_file_repo(test_dir):
    file = test_dir / "data.json"
    repo = FileRepository(connection={'filepath': file, 'key': 'url'})

    data = {"url": "1234.com", 'fields': "something"}
    id = repo.write(data)

    returned_data = repo.get_id(id)
    assert returned_data.get('url') == data.get('url')

def test_write_file_repo_data_integrity(test_dir):
    file = test_dir / "data.json"
    repo = FileRepository(connection={'filepath': file, 'key': 'url'})

    data = {"url": "1234.com", 'fields': "something"}
    _ = repo.write(data)

    with pytest.raises(DataIntegrityException): 
        repo.write(data)


def test_read_all_file_repo(test_dir):
    file = test_dir / "data.json"
    repo = FileRepository(connection={'filepath': file, 'key': 'url'})

    for i in range(4):
        data = {"url": f"{i}-1234.com", 'fields': "something"}
        _ = repo.write(data)

    returned_data = repo.read_all()
    # assert returned_data.get('url') == data.get('url')
    assert len(returned_data) == 4

def test_read_file_repo(test_dir):
    file = test_dir / "data.json"
    repo = FileRepository(connection={'filepath': file, 'key': 'url'})

    data = {"url": "1234.com", 'fields': "something"}
    _ = repo.write(data)

    returned_data = repo.read('1234.com')
    assert returned_data.get('fields') == data.get('fields')

def test_read_file_repo_no_found_value(test_dir):
    file = test_dir / "data.json"
    repo = FileRepository(connection={'filepath': file, 'key': 'url'})

    data = {"url": "1234.com", 'fields': "something"}
    _ = repo.write(data)

    returned_data = repo.read('notfound.com')
    assert returned_data == {}
