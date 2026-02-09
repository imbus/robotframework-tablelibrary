import csv
from pathlib import Path

import pytest

from Tables.utils.file_access import FileAccess
from Tables.utils.settings import (
    Delimiter,
    FileEncoding,
    FileType,
    LineTerminator,
    Quoting,
    QuotingCharacter,
)


class DummyLibrary:
    _file_type = FileType.CSV
    _separator = Delimiter[","]
    _file_encoding = FileEncoding.UTF_8.value
    _line_terminator = LineTerminator.LF
    _quoting = Quoting.MINIMAL
    _quoting_character = QuotingCharacter['"']
    _ignore_header = False


def _write_csv(path: Path, rows: list[list[str | int]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter=",")
        writer.writerows(rows)
    return path


@pytest.fixture
def library():
    return DummyLibrary()


@pytest.fixture
def file_access(library):
    return FileAccess(library)


@pytest.fixture
def write_csv():
    return _write_csv
