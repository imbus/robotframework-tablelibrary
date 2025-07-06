import pytest
from TableLibrary.keywords.getter import Getter
from TableLibrary.utils.settings import FileEncoding, FileType

class DummyLibrary:
    _file_encoding = FileEncoding.UTF8
    _file_type = FileType.CSV
    delimiter = ","
    ignore_header = False

@pytest.fixture
def getter():
    # LibraryAttributes expects a parent library, wir nutzen Dummy
    return Getter(DummyLibrary())

# ToDO
