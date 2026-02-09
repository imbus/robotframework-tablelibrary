from pathlib import Path

import pytest
from pandas import DataFrame

from Tables.utils.file_system import FileSync, TableObject
from Tables.utils.file_writer import FileWriter, ModifyAction
from Tables.utils.settings import (
    Delimiter,
    FileEncoding,
    FileType,
    LineTerminator,
    Quoting,
    QuotingCharacter,
    TableFormat,
)


class DummyLibrary:
    _file_type = FileType.CSV
    _separator = Delimiter[","]
    _file_encoding = FileEncoding.UTF_8.value
    _line_terminator = LineTerminator.LF
    _quoting = Quoting.MINIMAL
    _quoting_character = QuotingCharacter['"']
    _ignore_header = False


UPDATED_CELL_VALUE = 99
EXPECTED_ROW_COUNT_AFTER_REMOVE = 2
EXPECTED_COLUMN_COUNT_AFTER_APPEND = 3


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


def test_write_table_to_csv(tmp_path):
    writer = make_writer_with_table()
    path = tmp_path / "out.csv"
    data = [["h1", "h2"], [1, 2]]
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
