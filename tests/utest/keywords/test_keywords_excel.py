from pathlib import Path

import pandas as pd
import pytest

from Tables.keywords.excel import Excel
from Tables.utils.file_reader import FileReader
from Tables.utils.settings import FileType

SHEET_NAME = "Sheet1"
SHEET_DATA = [[1, 2], [3, 4]]
MISSING_SHEET = "Missing"


def test_excel_open_validates_file_type(library, tmp_path):
    library.scope_stack["file_type"].set(FileType.CSV)
    excel = Excel(library)
    path = tmp_path / "data.xlsx"
    path.touch()
    with pytest.raises(TypeError, match="Wrong file type configuration"):
        excel.excel_open("alias", path)


def test_excel_open_and_sheet_read(library, monkeypatch, tmp_path):
    library.scope_stack["file_type"].set(FileType.Excel)
    excel = Excel(library)
    path = tmp_path / "data.xlsx"
    path.touch()

    def fake_read_excel(self, file_path: Path, sheet_name=None):
        return {SHEET_NAME: pd.DataFrame(SHEET_DATA)}

    monkeypatch.setattr(FileReader, "read_excel", fake_read_excel)

    alias = excel.excel_open("book", path)
    assert alias == "book"
    assert excel.current_file == "book"

    available = excel.excel_get_available_sheets()
    assert SHEET_NAME in available

    data = excel.excel_sheet_read(SHEET_NAME)
    assert data == SHEET_DATA


def test_excel_close_and_get_open_files(library, monkeypatch, tmp_path):
    library.scope_stack["file_type"].set(FileType.Excel)
    excel = Excel(library)

    assert excel.excel_close() is False
    assert excel.excel_get_open_files() == []

    def fake_read_excel(self, file_path: Path, sheet_name=None):
        return {SHEET_NAME: pd.DataFrame(SHEET_DATA)}

    monkeypatch.setattr(FileReader, "read_excel", fake_read_excel)

    path = tmp_path / "data.xlsx"
    path.touch()

    excel.excel_open("book", path)
    assert excel.excel_get_open_files() == ["book"]

    assert excel.excel_close("book") is True
    assert excel.current_file is None


def test_excel_close_all_and_missing_alias(library, monkeypatch, tmp_path):
    library.scope_stack["file_type"].set(FileType.Excel)
    excel = Excel(library)

    def fake_read_excel(self, file_path: Path, sheet_name=None):
        return {SHEET_NAME: pd.DataFrame(SHEET_DATA)}

    monkeypatch.setattr(FileReader, "read_excel", fake_read_excel)

    path = tmp_path / "data.xlsx"
    path.touch()

    excel.excel_open("book", path)
    assert excel.excel_close() is True

    excel.excel_open("book", path)
    with pytest.raises(KeyError, match="Given file alias"):
        excel.excel_close("missing")


def test_excel_close_one_of_multiple(library, monkeypatch, tmp_path):
    library.scope_stack["file_type"].set(FileType.Excel)
    excel = Excel(library)

    def fake_read_excel(self, file_path: Path, sheet_name=None):
        return {SHEET_NAME: pd.DataFrame(SHEET_DATA)}

    monkeypatch.setattr(FileReader, "read_excel", fake_read_excel)

    path = tmp_path / "data.xlsx"
    path.touch()

    excel.excel_open("book_a", path)
    excel.excel_open("book_b", path)
    assert excel.excel_close("book_a") is True
    assert excel.current_file == "book_b"


def test_excel_file_switch_requires_multiple_files(library, monkeypatch, tmp_path):
    library.scope_stack["file_type"].set(FileType.Excel)
    excel = Excel(library)

    def fake_read_excel(self, file_path: Path, sheet_name=None):
        return {SHEET_NAME: pd.DataFrame(SHEET_DATA)}

    monkeypatch.setattr(FileReader, "read_excel", fake_read_excel)

    path = tmp_path / "data.xlsx"
    path.touch()

    excel.excel_open("book_a", path)
    with pytest.raises(KeyError, match="No or only one file is opened"):
        excel.excel_file_switch("book_a")

    excel.excel_open("book_b", path)
    excel.excel_file_switch("book_b")
    assert excel.current_file == "book_b"


def test_excel_sheet_read_missing_sheet(library, monkeypatch, tmp_path):
    library.scope_stack["file_type"].set(FileType.Excel)

    excel = Excel(library)

    def fake_read_excel(self, file_path: Path, sheet_name=None):
        return {SHEET_NAME: pd.DataFrame(SHEET_DATA)}

    monkeypatch.setattr(FileReader, "read_excel", fake_read_excel)

    path = tmp_path / "data.xlsx"
    path.touch()

    excel.excel_open("book", path)
    with pytest.raises(ValueError, match="Sheet 'Missing' not found"):
        excel.excel_sheet_read(MISSING_SHEET)
