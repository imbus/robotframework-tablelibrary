from pathlib import Path

import pandas as pd
import pytest
from pandas import DataFrame

from Tables.utils.file_reader import FileReader
from Tables.utils.file_system import FileSync
from Tables.utils.settings import (
    FileType,
    TableFormat,
)

from .helper.helpers import DummyLibrary

DEFAULT_HEADERS = ["A", "B"]
MISSING_COLUMN_NAME = "missing"
DATETIME_COLUMN = "ts"
EXPECTED_PARQUET_HEADER = ["c1", "c2"]


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
    reader.ignore_header_stack.set(True)
    df = DataFrame([["h1", "h2"], [1, 2]])
    with pytest.raises(TypeError):
        reader.validate_column(df, "h1")


def test_validate_column_with_header_row():
    reader = make_reader()
    reader.ignore_header_stack.set(False)
    df = DataFrame([["h1", "h2"], [1, 2]])
    assert reader.validate_column(df, "h1") is True
    with pytest.raises(IndexError):
        reader.validate_column(df, 5)
    with pytest.raises(ValueError, match="Couldn't find column"):
        reader.validate_column(df, MISSING_COLUMN_NAME)
    assert reader.validate_column(df, 1) is True
    assert reader.validate_column(df, 0) is True


def test_validate_column_in_bounds_int_returns_true():
    reader = make_reader()
    df = DataFrame([[1, 2], [3, 4]])
    assert reader.validate_column(df, 1) is True


def test_validate_column_int_branch_no_out_of_bounds():
    reader = make_reader()
    df = DataFrame([[1, 2, 3]])
    assert reader.validate_column(df, 0) is True


def test_validate_column_casts_numeric_string_to_int_in_bounds():
    reader = make_reader()
    df = DataFrame([[1]])
    assert reader.validate_column(df, "0") is True


def test_validate_row_bounds():
    reader = make_reader()
    df = DataFrame([[1, 2], [3, 4]])
    assert reader.validate_row(df, 1) is True
    with pytest.raises(IndexError):
        reader.validate_row(df, 5)


def test_validate_data_list_with_table():
    reader = make_reader()
    df = DataFrame([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError, match="Cannot ignore both row and column if selected data is a list"):
        reader.validate_data_list_with_table([1, 2], df)
    with pytest.raises(ValueError, match="Cannot select both row and column if selected data is a list"):
        reader.validate_data_list_with_table([1, 2], df, row=0, column=0)
    with pytest.raises(ValueError, match="Selected list is too small for the table"):
        reader.validate_data_list_with_table([1, 2], df, row=0)
    assert reader.validate_data_list_with_table([1, 2], df, column=0) is True


def test_convert_dataframe_list_of_lists_and_dicts():
    reader = make_reader()
    df = DataFrame([["h1", "h2"], [1, 2]])
    reader.file_type_stack.set(FileType.CSV)
    reader.ignore_header_stack.set(False)
    as_lists = reader.convert_dataframe(df, TableFormat["List of lists"])
    assert as_lists == [["h1", "h2"], [1, 2]]

    as_dicts = reader.convert_dataframe(df, TableFormat["List of dicts"])
    assert as_dicts == [{"h1": 1, "h2": 2}]


def test_convert_dataframe_list_of_dicts_ignores_header_logic_for_parquet():
    reader = make_reader()
    df = DataFrame([[1, 2]], columns=["h1", "h2"])
    reader.file_type_stack.set(FileType.Parquet)
    reader.ignore_header_stack.set(False)
    as_dicts = reader.convert_dataframe(df, TableFormat["List of dicts"])
    assert as_dicts == [{"h1": 1, "h2": 2}]


def test_convert_dataframe_parquet_inserts_header_row():
    reader = make_reader()
    df = DataFrame([[1, 2]], columns=["c1", "c2"])
    reader.file_type_stack.set(FileType.Parquet)
    reader.ignore_header_stack.set(False)
    as_lists = reader.convert_dataframe(df, TableFormat["List of lists"])
    assert as_lists[0] == ["c1", "c2"]


def test_convert_dataframe_returns_dataframe():
    reader = make_reader()
    df = DataFrame([[1, 2]])
    result = reader.convert_dataframe(df, TableFormat["Dataframe"])
    assert result.equals(df)


def test_convert_dataframe_invalid_format():
    reader = make_reader()
    df = DataFrame([[1, 2]])
    with pytest.raises(ValueError, match="Invalid TableFormat type"):
        reader.convert_dataframe(df, "bad")


def test_reset_header_dataframe_csv_moves_header_into_body():
    reader = make_reader()
    reader.file_type_stack.set(FileType.CSV)
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
    assert reader.file_type_stack.set(FileType.CSV)

    alias = reader.open_table_dataframe("t1", csv_path)
    assert alias == "t1"
    assert reader.current_alias == "t1"
    assert reader.opened_table_path == csv_path

    assert reader.close_table_dataframe("t1") is True
    assert reader.file_sync.current_file is None


def test_table_dataframe_switch_requires_two_tables(tmp_path):
    reader = make_reader()
    csv_path = tmp_path / "data.csv"
    pd.DataFrame([[1, 2]]).to_csv(csv_path, index=False, header=False)
    reader.open_table_dataframe("a", csv_path)
    with pytest.raises(KeyError):
        reader.table_dataframe_switch("a")


def test_opened_table_path_and_alias_errors():
    reader = make_reader()
    with pytest.raises(ValueError, match="No file path found"):
        _ = reader.opened_table_path
    with pytest.raises(ValueError, match="No file open"):
        _ = reader.current_alias


def test_file_exists_raises_for_missing_file(tmp_path):
    reader = make_reader()
    missing = tmp_path / "missing.csv"
    with pytest.raises(FileNotFoundError, match="File not found"):
        reader.file_exists(missing)


def test_reset_header_dataframe_parquet_default_header():
    reader = make_reader()
    reader.file_type_stack.set(FileType.Parquet)
    df = DataFrame([[DEFAULT_HEADERS[0], DEFAULT_HEADERS[1]], [1, 2]])
    reset = reader.reset_header_dataframe(df)
    assert list(reset.columns) == DEFAULT_HEADERS
    assert reset.iloc[0].tolist() == [1, 2]


def test_reset_header_dataframe_parquet_keeps_non_default_header():
    reader = make_reader()
    reader.file_type_stack.set(FileType.Parquet)
    df = DataFrame([[1, 2]], columns=["h1", "h2"])
    reset = reader.reset_header_dataframe(df)
    assert reset.equals(df)


def test_validate_table_to_dataframe_applies_header():
    reader = make_reader()
    reader.file_type_stack.set(FileType.CSV)
    data = [["h1", "h2"], [1, 2]]
    table = reader.validate_table_to_dataframe(data, column="h1")
    assert list(table.columns) == ["h1", "h2"]
    assert table.iloc[0].tolist() == [1, 2]


def test_read_excel_uses_pandas(monkeypatch, tmp_path):
    reader = make_reader()
    expected = DataFrame([[1, 2]])

    def fake_read_excel(path, header=None, sheet_name=0):
        return expected

    monkeypatch.setattr(pd, "read_excel", fake_read_excel)
    result = reader.read_excel(tmp_path / "data.xlsx")
    assert result.equals(expected)


def test_read_parquet_fallback(monkeypatch, tmp_path):
    reader = make_reader()
    expected = DataFrame([[1, 2]])

    def fake_read_parquet(path):
        return expected

    def bad_transform(df):
        raise RuntimeError("boom")

    monkeypatch.setattr(pd, "read_parquet", fake_read_parquet)
    monkeypatch.setattr(reader, "_parquet_transform_to_iso_timeformat", bad_transform)
    result = reader.read_parquet(tmp_path / "data.parquet")
    assert result.equals(expected)


def test_parquet_transform_to_iso_timeformat():
    reader = make_reader()
    df = DataFrame({DATETIME_COLUMN: pd.to_datetime(["2024-01-01T10:11:12.123Z"])})
    result = reader._parquet_transform_to_iso_timeformat(df)
    assert result[DATETIME_COLUMN].iloc[0].endswith("Z")


def test_read_table_file_unsupported_type(monkeypatch, tmp_path):
    reader = make_reader()
    path = tmp_path / "data.unknown"
    path.write_text("x")

    monkeypatch.setattr(reader, "read_data_type", lambda p: "bad")
    with pytest.raises(ValueError, match="Not supported data type"):
        reader.read_table_file(path)


def test_read_table_file_none_path():
    reader = make_reader()
    result = reader.read_table_file(None)
    assert result == {}


def test_close_table_dataframe_missing_alias(tmp_path):
    reader = make_reader()
    csv_path = tmp_path / "data.csv"
    pd.DataFrame([[1, 2]]).to_csv(csv_path, index=False, header=False)
    reader.open_table_dataframe("t1", csv_path)
    with pytest.raises(KeyError, match="Given file alias"):
        reader.close_table_dataframe("missing")


def test_close_table_dataframe_all(tmp_path):
    reader = make_reader()
    csv_path = tmp_path / "data.csv"
    pd.DataFrame([[1, 2]]).to_csv(csv_path, index=False, header=False)
    reader.open_table_dataframe("t1", csv_path)
    assert reader.close_table_dataframe() is True
    assert reader.file_sync.current_file is None


def test_close_table_dataframe_last_alias_clears_current(tmp_path):
    reader = make_reader()
    csv_path = tmp_path / "data.csv"
    pd.DataFrame([[1, 2]]).to_csv(csv_path, index=False, header=False)
    reader.open_table_dataframe("t1", csv_path)
    assert reader.close_table_dataframe("t1") is True
    assert reader.file_sync.current_file is None


def test_close_table_dataframe_keeps_current_when_other_tables_open(tmp_path):
    reader = make_reader()
    csv_path = tmp_path / "data.csv"
    pd.DataFrame([[1, 2]]).to_csv(csv_path, index=False, header=False)
    reader.open_table_dataframe("t1", csv_path)
    reader.open_table_dataframe("t2", csv_path)
    assert reader.close_table_dataframe("t1") is True
    assert reader.file_sync.current_file == "t2"


def test_table_dataframe_switch_success(tmp_path):
    reader = make_reader()
    csv_path = tmp_path / "data.csv"
    pd.DataFrame([[1, 2]]).to_csv(csv_path, index=False, header=False)
    reader.open_table_dataframe("a", csv_path)
    reader.open_table_dataframe("b", csv_path)
    assert reader.table_dataframe_switch("a") == "a"
