import pytest
from Tables.keywords.configuration import Configuration
from Tables.utils.settings import FileType, FileEncoding, Delimiter

class DummyLibrary:
    pass

@pytest.fixture
def config():
    # LibraryAttributes expects a parent library, we use a dummy
    return Configuration(DummyLibrary())

def test_set_file_type(config):
    config.configure_file_type(FileType.CSV)
    assert config.file_type == FileType.CSV

def test_set_delimiter(config):
    config.configure_delimiter(Delimiter[","])
    assert config.delimiter == Delimiter[","]

def test_set_file_encoding(config):
    config.configure_file_encoding(FileEncoding.UTF8)
    assert config.file_encoding == FileEncoding.UTF8

def test_set_ignore_header(config):
    config.configure_ignore_header(True)
    assert config.ignore_header is True
    config.configure_ignore_header(False)
    assert config.ignore_header is False
