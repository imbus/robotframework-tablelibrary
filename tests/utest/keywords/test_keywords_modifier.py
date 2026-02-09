import pytest

from Tables.keywords.modifier import Modifier

HEADER = ["h1", "h2"]
ROW_1 = ["a", "b"]
ROW_2 = ["c", "d"]
ROWS = [HEADER, ROW_1, ROW_2]
INSERTED_ROW = ["x", "y"]
INSERTED_COLUMN = ["col", "v1", "v2"]
EXPECTED_ROWS_AFTER_INSERT = 3
EXPECTED_COLUMNS_AFTER_INSERT = 3
EXPECTED_ROWS_AFTER_REMOVE = 2
EXPECTED_COLUMNS_AFTER_REMOVE = 2


@pytest.fixture
def modifier(library, file_access, tmp_path, write_csv):
    path = tmp_path / "data.csv"

    write_csv(path, ROWS)
    file_access.file_reader.open_table_dataframe("table", path)
    return Modifier(library, file_access)


def test_insert_row(modifier):
    table = modifier.insert_row(INSERTED_ROW, row_index=1, header=True)
    assert table.shape[0] == EXPECTED_ROWS_AFTER_INSERT


def test_insert_column(modifier):
    table = modifier.insert_column(INSERTED_COLUMN, column_index=1)
    assert table.shape[1] == EXPECTED_COLUMNS_AFTER_INSERT


def test_append_and_remove_row(modifier):
    appended = modifier.append_row(["m", "n"])
    assert appended.iloc[-1].tolist() == ["m", "n"]

    removed = modifier.remove_row(0, header=True)
    assert removed.shape[0] == EXPECTED_ROWS_AFTER_REMOVE


def test_append_and_remove_column(modifier):
    appended = modifier.append_column(["h3", "e", "f"])
    assert appended.shape[1] == EXPECTED_COLUMNS_AFTER_INSERT

    removed = modifier.remove_column(0)
    assert removed.shape[1] == EXPECTED_COLUMNS_AFTER_REMOVE
