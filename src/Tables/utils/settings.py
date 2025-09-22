import csv
from enum import Enum

class Quoting(Enum):
    """
    Available quoting options for CSV mainly. Default is MINIMAL.
    """
    ALL = csv.QUOTE_ALL
    MINIMAL = csv.QUOTE_MINIMAL
    NONNUMERIC = csv.QUOTE_NONNUMERIC
    NONE = csv.QUOTE_NONE

QuotingCharacter = Enum(
    "QuotingCharacter",
    {
        "\"": "\"",
        "'": "'",
    }
)
QuotingCharacter.__doc__ = """
    Available quoting characters - default is ``\"``.
    | = Delimiter = | = Description = |
    | ``\"`` | Using the \" as separator. |
    | ``'`` | Using the ' as separator. |
"""

TableFormat = Enum(
    "TableFormat",
    {
        "List of lists": 0,
        "List of dicts": 1,
        "Dataframe": 2,
    }
)

TableFormat.__doc__ = """
    Available table formats. Mostly used as return type during reading/getting the table.
    | = Delimiter = | = Description = |
    | ``List of lists`` | Using the table format as list[list] |
    | ``List of dicts`` | Using the table format as list[dict] |
    | ``Dataframe``     | Using the table format as pandas.DataFrame |
"""

class FileType(Enum):
    """
    Available file types / extension for your input files.
    """
    CSV = "csv"
    Excel = "xlsx"
    Parquet = "parquet"
    List_of_lists = "0"

class FileSuffix(Enum):
    """
    Available file suffix for related file types.
    """
    TXT = "txt"
    CSV = "csv"
    TSV = "tsv"
    XLSX = "xlsx"
    XLS = "xls"
    Parquet = "parquet"

class FileEncoding(Enum):
    """
    Available file encodings for working with table files.
    """
    UTF8 = "utf-8"
    UTF16 = "utf-16"
    LATIN1 = "latin-1"

class LineTerminator(Enum):
    """
    Available line terminators.
    """
    LF = "\n"
    CRLR = "\r\n"

Delimiter = Enum(
    "Delimiter",
    {
        ";": ";",
        ",": ",",
        "\t": "\t",
    }
)
Delimiter.__doc__ = """
    Available separators for splitting data columns in any table file - default is ``,``.
    | = Delimiter = | = Description = |
    | ``;`` | Using the semicolon as separator. |
    | ``,`` | Using the comma as separator. |
    | ``\\t`` | Using the ``tab`` character as separator. |
    | ... | In case of any missing separator, feel free to add it... |
"""

DecimalSeperator = Enum(
    "DecimalSeperator",
    {
        ".": ".",
        ",": ","
    }
)
DecimalSeperator.__doc__ = """
    Available decimal seperators.
"""
