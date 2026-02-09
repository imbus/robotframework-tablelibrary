from pathlib import Path

import pytest

from Tables.keywords.writer import Writer
HEADER = ["h1", "h2"]
ROW_1 = ["a", "b"]
ROW_2 = ["c", "d"]
ROWS = [HEADER, ROW_1, ROW_2]
UPDATED_VALUE = "z"
UPDATED_ROW = ["m", "n"]
UPDATED_COLUMN = ["h2", "x", "y"]


@pytest.fixture
def writer(library, file_access):
    return Writer(library, file_access)


@pytest.fixture
def opened_table(file_access, tmp_path, write_csv):
    path = tmp_path / "data.csv"

    write_csv(path, ROWS)
    file_access.file_reader.open_table_dataframe("table", path)
    return path


def test_write_table_creates_file(writer, tmp_path):
    output = tmp_path / "out.csv"
    result = writer.write_table(ROWS, output)
    assert Path(result).exists()


def test_write_table_from_alias(writer, opened_table, tmp_path):
    output = tmp_path / "out_alias.csv"
    result = writer.write_table("table", output)
    assert Path(result).exists()


def test_set_table_cell(writer, opened_table):
    result = writer.set_table_cell(UPDATED_VALUE, row=0, column="h1", header=True)
    assert result[0][0] == "h1"
    assert result[1][0] == UPDATED_VALUE


def test_set_table_row(writer, opened_table):
    table = writer.set_table_row(UPDATED_ROW, row=0, header=True)
    assert table[1] == UPDATED_ROW


def test_set_table_column(writer, opened_table):
    table = writer.set_table_column(UPDATED_COLUMN, column=1, header=False)
    assert table[0][1] == UPDATED_COLUMN[0]


def test_writer_fs_property(writer):
    assert writer._fs is not None
