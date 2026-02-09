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


def test_file_access_shares_sync_between_reader_and_writer():
    access = FileAccess(DummyLibrary())
    assert access.file_reader.file_sync is access.file_writer.file_sync
