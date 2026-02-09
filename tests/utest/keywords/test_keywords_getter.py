from pathlib import Path

import pandas as pd
import pytest
from assertionengine import AssertionOperator
from robot.api.exceptions import ContinuableFailure

from Tables.keywords.getter import Getter
from Tables.utils.file_reader import Axis
from Tables.utils.settings import FileType, TableFormat

HEADER = ["h1", "h2"]
ROW_1 = ["a", "b"]
ROW_2 = ["c", "d"]
ROWS = [HEADER, ROW_1, ROW_2]
EXPECTED_ROW_COUNT = 3
EXPECTED_COLUMN_COUNT = 2
EXPECTED_PARQUET_ROWS = 3


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


def test_read_table_ignore_header(getter, tmp_path, write_csv):
    path = tmp_path / "data.csv"
    write_csv(path, ROWS)
    getter.library._ignore_header = True

    data = getter.read_table(path, TableFormat["List of lists"])
    assert data == [ROW_1, ROW_2]


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


def test_getter_ignore_header(getter, tmp_path, write_csv):
    path = tmp_path / "data.csv"
    write_csv(path, ROWS)
    getter.library._ignore_header = True

    getter.open_table(path, alias="t_ignore")
    table = getter.get_table()
    assert table == [ROW_1, ROW_2]


def test_getter_invalid_assertion_operator(getter, tmp_path, write_csv):
    path = tmp_path / "data.csv"
    write_csv(path, ROWS)
    getter.open_table(path, alias="t_ops")

    with pytest.raises(ValueError, match="Unexpected operator for assertion"):
        getter.get_table_cell(0, "h1", assertion_operator="bad", assertion_expected="a")

    with pytest.raises(ValueError, match="Unexpected operator for assertion"):
        getter.get_table_column("h1", assertion_operator="bad", assertion_expected="a")

    with pytest.raises(ValueError, match="Unexpected operator for assertion"):
        getter.count_table("t_ops", Axis.Rows, assertion_operator="bad", assertion_expected=1)


def test_getter_close_and_switch_errors(getter, tmp_path, write_csv):
    assert getter.close_table() is False

    path = tmp_path / "data.csv"
    write_csv(path, ROWS)
    getter.open_table(path, alias="t_single")
    with pytest.raises(KeyError, match="No or only one file is opened"):
        getter.switch_table("t_single")


def test_getter_switch_table_success(getter, tmp_path, write_csv):
    path = tmp_path / "data.csv"
    write_csv(path, ROWS)
    getter.open_table(path, alias="t1")
    getter.open_table(path, alias="t2")
    assert getter.switch_table("t1") == "t1"


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


def test_open_and_create_table_without_alias(getter, tmp_path, write_csv):
    path = tmp_path / "data.csv"
    write_csv(path, ROWS)

    alias = getter.open_table(path)
    assert alias

    table_alias = getter.create_table(["a", "b"])
    assert table_alias


def test_getter_internal_fs_property(getter):
    assert getter._fs is not None


def test_get_table_returns_dataframe(getter, tmp_path, write_csv):
    path = tmp_path / "data.csv"
    write_csv(path, ROWS)
    getter.open_table(path, alias="t_df")

    data = getter.get_table(TableFormat["Dataframe"])
    assert isinstance(data, pd.DataFrame)


def test_getter_assertion_success_paths(getter, tmp_path, write_csv):
    path = tmp_path / "data.csv"
    write_csv(path, ROWS)
    getter.open_table(path, alias="t_assert")

    getter.get_table_cell(0, "h1", assertion_operator=AssertionOperator["=="], assertion_expected="a")
    getter.get_table_column(
        "h2",
        assertion_operator=AssertionOperator["contains"],
        assertion_expected="b",
    )
    getter.get_table_row(
        1,
        assertion_operator=AssertionOperator["contains"],
        assertion_expected="a",
    )


def test_count_table_parquet_assertions(getter, tmp_path, monkeypatch):
    getter.file_type = FileType.Parquet

    def fake_read_table_file(path: Path):
        return pd.DataFrame([[1, 2], [3, 4]], columns=["c1", "c2"])

    monkeypatch.setattr(getter.file_reader, "read_table_file", fake_read_table_file)

    count = getter.count_table(tmp_path / "data.parquet", Axis.Rows)
    assert count == EXPECTED_PARQUET_ROWS

    with pytest.raises(AssertionError):
        getter.count_table(
            tmp_path / "data.parquet",
            Axis.Columns,
            assertion_operator=AssertionOperator["=="],
            assertion_expected=99,
            continue_on_failure=False,
        )

    with pytest.raises(ContinuableFailure):
        getter.count_table(
            tmp_path / "data.parquet",
            Axis.Columns,
            assertion_operator=AssertionOperator["=="],
            assertion_expected=99,
            continue_on_failure=True,
        )
