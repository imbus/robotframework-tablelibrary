from pathlib import Path

import pandas as pd
import pytest
from pandas import DataFrame

from Tables.utils.file_reader import FileReader
from Tables.utils.file_system import FileSync, TableObject
from Tables.utils.file_writer import FileWriter, ModifyAction
from Tables.utils.settings import (
    FileType,
    TableFormat,
)

from .helper.helpers import DummyLibrary

UPDATED_CELL_VALUE = 99
EXPECTED_ROW_COUNT_AFTER_REMOVE = 2
EXPECTED_COLUMN_COUNT_AFTER_APPEND = 3
PARQUET_COLUMNS = ["c1", "c2"]
INVALID_FILE_PATH = "not-a-path"
EXPECTED_SINGLE_COLUMN_INDEX = [0]


def make_writer_with_table():
    sync = FileSync()
    df = DataFrame([["h1", "h2"], [1, 2], [3, 4]])
    sync.table_storage["t1"] = TableObject(Path("dummy.csv"), df)
    sync.current_file = "t1"
    return FileWriter(DummyLibrary(), sync)


def test_find_file_path_with_alias():
    writer = make_writer_with_table()
    assert writer.find_file_path("t1").name == "dummy.csv"


def test_insert_row_and_column():
    writer = make_writer_with_table()
    table = writer.add_header_in_dataframe(writer.current_table.data)
    updated = writer.insert_row_to_dataframe(1, ["x", "y"], table)
    assert updated.iloc[1].tolist() == ["x", "y"]

    updated = writer.insert_column_to_dataframe(1, [10, 20, 30], table)
    assert updated.shape[1] == EXPECTED_COLUMN_COUNT_AFTER_APPEND

    with pytest.raises(ValueError, match="Cannot insert row"):
        writer.insert_row_to_dataframe(None, ["x"], table)


def test_insert_column_parquet_skips_header_reset():
    writer = make_writer_with_table()
    writer.file_type = FileType.Parquet
    table = writer.current_table.data
    updated = writer.insert_column_to_dataframe(0, [9, 8, 7], table)
    assert updated.shape[1] == EXPECTED_COLUMN_COUNT_AFTER_APPEND


def test_append_and_remove_row_column():
    writer = make_writer_with_table()
    table = writer.add_header_in_dataframe(writer.current_table.data)
    appended = writer.append_row_to_dataframe(["z", "w"], table)
    assert appended.iloc[-1].tolist() == ["z", "w"]

    appended = writer.append_column_to_dataframe([9, 8, 7, 6], table)
    assert appended.shape[1] == EXPECTED_COLUMN_COUNT_AFTER_APPEND

    removed_col = writer.remove_column_dataframe(0, table)
    assert removed_col.shape[1] == 1

    removed_row = writer.remove_row_dataframe(0, table)
    assert removed_row.shape[0] == EXPECTED_ROW_COUNT_AFTER_REMOVE


def test_append_column_parquet_skips_header_reset():
    writer = make_writer_with_table()
    writer.file_type = FileType.Parquet
    table = writer.current_table.data
    updated = writer.append_column_to_dataframe([9, 8, 7], table)
    assert updated.shape[1] == EXPECTED_COLUMN_COUNT_AFTER_APPEND


def test_write_table_to_csv(tmp_path):
    writer = make_writer_with_table()
    path = tmp_path / "out.csv"
    data = [["h1", "h2"], [1, 2]]
    out = writer.write_table(data, path)
    assert out.exists()


def test_write_table_dataframe(tmp_path):
    writer = make_writer_with_table()
    path = tmp_path / "out.csv"
    data = DataFrame([[1, 2]])
    out = writer.write_table(data, path)
    assert out.exists()


def test_write_table_parquet_list(tmp_path, monkeypatch):
    writer = make_writer_with_table()
    writer.file_type = FileType.Parquet
    path = tmp_path / "out.parquet"
    data = [PARQUET_COLUMNS, [1, 2]]

    def fake_to_parquet(self, file_path):
        Path(file_path).write_text("parquet")

    monkeypatch.setattr(pd.DataFrame, "to_parquet", fake_to_parquet)
    out = writer.write_table(data, path)
    assert out.exists()


def test_set_dataframe_cells_updates_cached_dataframe():
    writer = make_writer_with_table()
    result = writer.set_dataframe_cells(
        data=UPDATED_CELL_VALUE,
        row=0,
        column="h1",
        header=True,
        return_type=TableFormat["List of lists"],
    )
    assert result[0][0] == "h1"
    assert result[1][0] == UPDATED_CELL_VALUE


def test_modify_table_append_row():
    writer = make_writer_with_table()
    table = writer.modify_table(ModifyAction.Append_Row, data=[5, 6], header=True)
    assert table.iloc[-1].tolist() == [5, 6]


def test_modify_table_invalid_action():
    writer = make_writer_with_table()
    with pytest.raises(ValueError, match="Invalid action"):
        writer.modify_table("bad")


def test_find_file_path_with_none_uses_current():
    writer = make_writer_with_table()
    assert writer.find_file_path().name == "dummy.csv"


def test_add_header_in_dataframe_parquet():
    writer = make_writer_with_table()
    writer.file_type = FileType.Parquet
    df = DataFrame([[1, 2]], columns=PARQUET_COLUMNS)
    result = writer.add_header_in_dataframe(df)
    assert list(result.columns) == PARQUET_COLUMNS
    assert result.iloc[0].tolist() == [1, 2]


def test_insert_column_rejects_invalid_inputs():
    writer = make_writer_with_table()
    table = writer.add_header_in_dataframe(writer.current_table.data)
    with pytest.raises(ValueError, match="Cannot insert column"):
        writer.insert_column_to_dataframe(None, [1], table)
    with pytest.raises(TypeError, match="Cannot modify table using column name"):
        writer.insert_column_to_dataframe("h1", [1, 2], table)


def test_append_column_and_row_reject_none():
    writer = make_writer_with_table()
    table = writer.add_header_in_dataframe(writer.current_table.data)
    with pytest.raises(ValueError, match="Cannot append column"):
        writer.append_column_to_dataframe(None, table)
    with pytest.raises(ValueError, match="Cannot append row"):
        writer.append_row_to_dataframe(None, table)


def test_remove_column_and_row_reject_none():
    writer = make_writer_with_table()
    table = writer.add_header_in_dataframe(writer.current_table.data)
    with pytest.raises(ValueError, match="Cannot remove column"):
        writer.remove_column_dataframe(None, table)
    with pytest.raises(ValueError, match="Cannot remove row"):
        writer.remove_row_dataframe(None, table)


def test_remove_column_resets_index_when_no_header():
    writer = make_writer_with_table()
    writer.header = False
    table = writer.add_header_in_dataframe(writer.current_table.data)
    removed = writer.remove_column_dataframe(0, table)
    assert list(removed.columns) == EXPECTED_SINGLE_COLUMN_INDEX


def test_write_table_invalid_path_type(monkeypatch):
    writer = make_writer_with_table()
    monkeypatch.setattr(writer, "find_file_path", lambda p=None: INVALID_FILE_PATH)
    with pytest.raises(TypeError, match="Invalid file_path type"):
        writer.write_table([["h1"]], "ignored.csv")


def test_write_table_invalid_file_type(monkeypatch, tmp_path):
    writer = make_writer_with_table()
    path = tmp_path / "out.csv"

    monkeypatch.setattr(FileReader, "read_data_type", lambda self, p: "bad")
    with pytest.raises(ValueError, match="Unsupported file type"):
        writer.write_table([["h1"]], path)


def test_set_dataframe_cells_validates_row():
    writer = make_writer_with_table()
    result = writer.set_dataframe_cells(
        data=UPDATED_CELL_VALUE,
        row=1,
        column="h1",
        header=True,
        return_type=TableFormat["List of lists"],
    )
    assert result[2][0] == UPDATED_CELL_VALUE


def test_update_cached_dataframe_without_current_file(monkeypatch):
    writer = make_writer_with_table()
    writer.file_sync.current_file = None
    df = DataFrame([[1, 2]])

    dummy = TableObject(Path("dummy.csv"), DataFrame([[1]]))
    monkeypatch.setattr(FileWriter, "current_table", property(lambda self: dummy))

    result = writer.update_cached_dataframe(df)
    assert result.equals(dummy.data)
