from Tables import Tables
from Tables.utils.settings import (
    Delimiter,
    FileEncoding,
    FileType,
    LineTerminator,
    Quoting,
    QuotingCharacter,
)


def test_tables_init_defaults():
    tables = Tables()
    assert tables._file_type == FileType.CSV
    assert tables._separator == Delimiter[","]
    assert tables._file_encoding == FileEncoding.UTF_8.value
    assert tables.scope_stack["ignore_header"].get() is False
    assert tables._line_terminator == LineTerminator.LF
    assert tables._quoting == Quoting.MINIMAL
    assert tables._quoting_character == QuotingCharacter['"']
    assert tables.file_access is not None


def test_tables_init_custom_values():
    tables = Tables(
        file_type=FileType.Excel,
        file_encoding="latin_1",
        separator=Delimiter[";"],
        ignore_header=True,
        line_terminator=LineTerminator.CRLR,
        quoting=Quoting.NONE,
        quoting_character=QuotingCharacter["'"],
    )
    assert tables._file_type == FileType.Excel
    assert tables._separator == Delimiter[";"]
    assert tables._file_encoding == "latin_1"
    assert tables.scope_stack["ignore_header"].get() is True
    assert tables._line_terminator == LineTerminator.CRLR
    assert tables._quoting == Quoting.NONE
    assert tables._quoting_character == QuotingCharacter["'"]
