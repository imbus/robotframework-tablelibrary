import pytest
from TableLibrary.keywords.configuration import Configuration
from TableLibrary.utils.settings import FileType, FileEncoding, Delimiter

class DummyLibrary:
    pass

@pytest.fixture
def config():
    # LibraryAttributes expects a parent library, we use a dummy
    return Configuration(DummyLibrary())

def test_set_file_type(config):
    config.set_file_type(FileType.CSV)
    assert config.file_type == FileType.CSV.value

def test_set_delimiter(config):
    config.set_delimiter(Delimiter[","])
    assert config.delimiter == Delimiter[","].value

def test_set_file_encoding(config):
    config.set_file_encoding(FileEncoding.UTF8)
    assert config.file_encoding == FileEncoding.UTF8.value

def test_set_ignore_header(config):
    config.set_ignore_header(True)
    assert config.ignore_header is True
    config.set_ignore_header(False)
    assert config.ignore_header is False
