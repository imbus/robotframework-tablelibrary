from enum import Enum

class FileType(Enum):
    """
    Available file types / extension for your input files.
    """
    CSV = "csv"
    Excel = "xlsx"
    Parquet = "parquet"

class FileSuffix(Enum):
    """
    Available file suffix for related file types.
    """
    CSV = "csv"
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
