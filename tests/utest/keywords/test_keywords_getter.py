from pathlib import Path

import pandas as pd
import pytest

from Tables.keywords.getter import Getter
from Tables.utils.file_reader import Axis
from Tables.utils.settings import FileType, TableFormat

HEADER = ["h1", "h2"]
ROW_1 = ["a", "b"]
ROW_2 = ["c", "d"]
ROWS = [HEADER, ROW_1, ROW_2]
EXPECTED_ROW_COUNT = 3
EXPECTED_COLUMN_COUNT = 2


@pytest.fixture
def getter(library, file_access):
    return Getter(library, file_access)


def test_read_table_returns_list_of_lists(getter, tmp_path, write_csv):
    path = tmp_path / "data.csv"

    write_csv(path, ROWS)

    data = getter.read_table(path, TableFormat["List of lists"])
    assert data == ROWS


def test_read_table_returns_list_of_dicts(getter, tmp_path, write_csv):
    path = tmp_path / "data.csv"

    write_csv(path, ROWS)

    data = getter.read_table(path, TableFormat["List of dicts"])
    assert data == [
        {"h1": "a", "h2": "b"},
        {"h1": "c", "h2": "d"},
    ]


def test_read_table_returns_dataframe(getter, tmp_path, write_csv):
    path = tmp_path / "data.csv"

    write_csv(path, ROWS)

    data = getter.read_table(path, TableFormat["Dataframe"])
    assert isinstance(data, pd.DataFrame)


def test_open_get_table_and_cell_access(getter, tmp_path, write_csv):
    path = tmp_path / "data.csv"

    write_csv(path, ROWS)

    alias = getter.open_table(path, alias="t1")
    assert alias == "t1"

    table = getter.get_table()
    assert table == ROWS

    cell = getter.get_table_cell(0, "h1")
    assert cell == "a"

    column = getter.get_table_column("h2")
    assert column == ["b", "d"]

    row = getter.get_table_row(1)
    assert row == ROW_1


def test_count_table_by_path_and_alias(getter, tmp_path, write_csv):
    path = tmp_path / "data.csv"

    write_csv(path, ROWS)

    row_count = getter.count_table(path, Axis.Rows)
    column_count = getter.count_table(path, Axis.Columns)
    assert row_count == EXPECTED_ROW_COUNT
    assert column_count == EXPECTED_COLUMN_COUNT

    alias = getter.open_table(path, alias="t2")
    alias_row_count = getter.count_table(alias, Axis.Rows)
    assert alias_row_count == EXPECTED_ROW_COUNT


def test_read_table_parquet_header_handling(getter, tmp_path, monkeypatch):
    getter.file_type = FileType.Parquet

    def fake_read_table_file(path: Path):
        return pd.DataFrame([["x", "y"], ["m", "n"]], columns=["c1", "c2"])

    monkeypatch.setattr(getter.file_reader, "read_table_file", fake_read_table_file)

    data = getter.read_table(tmp_path / "data.parquet", TableFormat["List of lists"])
    assert data[0] == ["c1", "c2"]
