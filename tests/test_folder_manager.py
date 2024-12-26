from pathlib import Path
from jobsearch.folder_manager import LocalFolder

def test_local_folder():
    test_dir = Path.home() / 'test'
    lf = LocalFolder(working_folder=test_dir)

    lf.create_folder('20241225_data_engineer')

    assert len(list(test_dir.glob('*'))) == 1
