import pytest

from Tables.keywords.getter import Getter
from Tables.utils.settings import FileEncoding, FileType


class DummyLibrary:
    _file_encoding = FileEncoding.UTF_8
    _file_type = FileType.CSV
    separator = ","
    ignore_header = False


@pytest.fixture
def getter():
    # LibraryAttributes expects a parent library, wir nutzen Dummy
    return Getter(DummyLibrary())


# ToDO
