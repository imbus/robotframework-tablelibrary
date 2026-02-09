import pytest

from Tables.keywords.configuration import Configuration
from Tables.utils.settings import (
    Delimiter,
    FileEncoding,
    FileType,
    LineTerminator,
    Quoting,
    QuotingCharacter,
)


@pytest.fixture
def config(library):
    return Configuration(library)


def test_configuration_updates_file_type(config):
    config.configure_file_type(FileType.Excel)
    assert config.file_type == FileType.Excel


def test_configuration_updates_separator(config):
    config.configure_separator(Delimiter[","])
    assert config.separator == Delimiter[","]


def test_configuration_updates_quoting(config):
    config.configure_quoting(Quoting.MINIMAL)
    assert config.quoting == Quoting.MINIMAL


def test_configuration_updates_quoting_character(config):
    config.configure_quoting_character(QuotingCharacter['"'])
    assert config.quoting_character == QuotingCharacter['"']


def test_configuration_updates_line_terminator(config):
    config.configure_line_terminator(LineTerminator.LF)
    assert config.line_terminator == LineTerminator.LF


def test_configuration_updates_file_encoding(config):
    config.configure_file_encoding(FileEncoding.UTF_8)
    assert config.file_encoding == FileEncoding.UTF_8.value


def test_configuration_updates_ignore_header(config):
    config.configure_ignore_header(True)
    assert config.ignore_header is True
