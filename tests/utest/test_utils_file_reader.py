from pathlib import Path

import pandas as pd
import pytest
from pandas import DataFrame

from Tables.utils.file_reader import FileReader
from Tables.utils.file_system import FileSync
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


EXPECTED_TABLE_SHAPE = (2, 2)
EXPECTED_NUMERIC_CAST = 3


def make_reader():
    return FileReader(DummyLibrary(), FileSync())


def test_cast_column_type():
    reader = make_reader()
    assert reader.cast_column_type("3") == EXPECTED_NUMERIC_CAST
    assert reader.cast_column_type("a") == "a"


def test_validate_column_rejects_str_when_ignore_header_true():
    reader = make_reader()
    reader.ignore_header = True
    df = DataFrame([["h1", "h2"], [1, 2]])
    with pytest.raises(TypeError):
        reader.validate_column(df, "h1")


def test_validate_column_with_header_row():
    reader = make_reader()
    reader.ignore_header = False
    df = DataFrame([["h1", "h2"], [1, 2]])
    assert reader.validate_column(df, "h1") is True
    with pytest.raises(IndexError):
        reader.validate_column(df, 5)


def test_validate_row_bounds():
    reader = make_reader()
    df = DataFrame([[1, 2], [3, 4]])
    assert reader.validate_row(df, 1) is True
    with pytest.raises(IndexError):
        reader.validate_row(df, 5)


def test_validate_data_list_with_table():
    reader = make_reader()
    df = DataFrame([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(
        ValueError, match="Cannot ignore both row and column if selected data is a list"
    ):
        reader.validate_data_list_with_table([1, 2], df)
    with pytest.raises(
        ValueError, match="Cannot select both row and column if selected data is a list"
    ):
        reader.validate_data_list_with_table([1, 2], df, row=0, column=0)
    with pytest.raises(ValueError, match="Selected list is too small for the table"):
        reader.validate_data_list_with_table([1, 2], df, row=0)
    assert reader.validate_data_list_with_table([1, 2], df, column=0) is True


def test_convert_dataframe_list_of_lists_and_dicts():
    reader = make_reader()
    df = DataFrame([["h1", "h2"], [1, 2]])
    reader.file_type = FileType.CSV
    reader.ignore_header = False
    as_lists = reader.convert_dataframe(df, TableFormat["List of lists"])
    assert as_lists == [["h1", "h2"], [1, 2]]

    as_dicts = reader.convert_dataframe(df, TableFormat["List of dicts"])
    assert as_dicts == [{"h1": 1, "h2": 2}]


def test_convert_dataframe_parquet_inserts_header_row():
    reader = make_reader()
    df = DataFrame([[1, 2]], columns=["c1", "c2"])
    reader.file_type = FileType.Parquet
    reader.ignore_header = False
    as_lists = reader.convert_dataframe(df, TableFormat["List of lists"])
    assert as_lists[0] == ["c1", "c2"]


def test_reset_header_dataframe_csv_moves_header_into_body():
    reader = make_reader()
    reader.file_type = FileType.CSV
    df = DataFrame([[1, 2], [3, 4]], columns=["A", "B"])
    reset = reader.reset_header_dataframe(df)
    assert reset.iloc[0].tolist() == ["A", "B"]


def test_check_default_dataframe_header():
    reader = make_reader()
    df = DataFrame([[1, 2], [3, 4]])
    assert reader.check_default_dataframe_header(df) is True


def test_read_data_type():
    reader = make_reader()
    assert reader.read_data_type(Path("file.csv")) == FileType.CSV
    assert reader.read_data_type(Path("file.xlsx")) == FileType.Excel
    assert reader.read_data_type(Path("file.parquet")) == FileType.Parquet
    with pytest.raises(TypeError):
        reader.read_data_type(Path("file.unknown"))


def test_cast_path_type(tmp_path):
    reader = make_reader()
    existing = tmp_path / "a.csv"
    existing.write_text("a,b")
    assert isinstance(reader.cast_path_type(str(existing)), Path)
    missing = tmp_path / "missing.csv"
    assert reader.cast_path_type(str(missing)) == str(missing)


def test_read_table_file_and_open_close(tmp_path):
    reader = make_reader()
    csv_path = tmp_path / "data.csv"
    pd.DataFrame([[1, 2], [3, 4]]).to_csv(csv_path, index=False, header=False)

    table = reader.read_table_file(csv_path)
    assert table.shape == EXPECTED_TABLE_SHAPE
    assert reader.file_type == FileType.CSV

    alias = reader.open_table_dataframe("t1", csv_path)
    assert alias == "t1"
    assert reader.current_alias == "t1"

    assert reader.close_table_dataframe("t1") is True
    assert reader.file_sync.current_file is None


def test_table_dataframe_switch_requires_two_tables(tmp_path):
    reader = make_reader()
    csv_path = tmp_path / "data.csv"
    pd.DataFrame([[1, 2]]).to_csv(csv_path, index=False, header=False)
    reader.open_table_dataframe("a", csv_path)
    with pytest.raises(KeyError):
        reader.table_dataframe_switch("a")
