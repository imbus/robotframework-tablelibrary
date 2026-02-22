import csv
from pathlib import Path

import pytest

from Tables.utils.file_access import FileAccess

from ..helper.helpers import DummyLibrary


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
