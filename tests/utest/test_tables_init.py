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
    assert tables.scope_stack["file_type"].get() == FileType.CSV
    assert tables.scope_stack["separator"].get() == Delimiter[","]
    assert tables.scope_stack["file_encoding"].get() == FileEncoding.UTF_8.value
    assert tables.scope_stack["ignore_header"].get() is False
    assert tables.scope_stack["line_terminator"].get() == LineTerminator.LF
    assert tables.scope_stack["quoting"].get() == Quoting.MINIMAL
    assert tables.scope_stack["quoting_character"].get() == QuotingCharacter['"']
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
    assert tables.scope_stack["file_type"].get() == FileType.Excel
    assert tables.scope_stack["separator"].get() == Delimiter[";"]
    assert tables.scope_stack["file_encoding"].get() == "latin_1"
    assert tables.scope_stack["ignore_header"].get() is True
    assert tables.scope_stack["line_terminator"].get() == LineTerminator.CRLR
    assert tables.scope_stack["quoting"].get() == Quoting.NONE
    assert tables.scope_stack["quoting_character"].get() == QuotingCharacter["'"]
