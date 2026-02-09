from pathlib import Path

from pandas import DataFrame

from Tables.utils.file_system import FileSync, FileSystem, TableObject


def test_file_system_ensure_directory_exists(tmp_path):
    target = tmp_path / "new_dir"
    fs = FileSystem()
    assert fs.ensure_directory_exists(target) is True
    assert target.exists()


def test_file_sync_starts_empty():
    sync = FileSync()
    assert sync.table_storage == {}
    assert sync.current_file is None


def test_table_object_holds_data():
    df = DataFrame([[1, 2], [3, 4]])
    obj = TableObject(Path("dummy"), df)
    assert obj.path.name == "dummy"
    assert obj.data.equals(df)
