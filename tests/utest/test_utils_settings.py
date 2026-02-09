from Tables.utils.settings import (
    DecimalSeperator,
    Delimiter,
    FileEncoding,
    FileSuffix,
    FileType,
    LineTerminator,
    Quoting,
    QuotingCharacter,
    TableFormat,
)


def test_settings_enums_have_expected_values():
    assert FileType.CSV.value == "csv"
    assert FileSuffix.XLSX.value == "xlsx"
    assert FileEncoding.UTF_8.value == "utf_8"
    assert LineTerminator.LF.value == "\n"
    assert Delimiter[","].value == ","
    assert DecimalSeperator["."].value == "."
    assert Quoting.MINIMAL.value is not None
    assert QuotingCharacter['"'].value == '"'
    assert TableFormat["List of lists"].value == 0
