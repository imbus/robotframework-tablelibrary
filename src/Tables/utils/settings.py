from enum import Enum

class FileType(Enum):
    """
    Available file types / extension for your input files.
    """
    CSV = "csv"
    Excel = "excel"
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
    Available delimiters for splitting data columns in any table file - default is ``,``.
    | = Delimiter = | = Description = |
    | ``;`` | Using the semicolon as delimiter. |
    | ``,`` | Using the comma as delimiter. |
    | ``\\t`` | Using the ``tab`` character as delimiter. |
    | ... | In case of any missing delimiter, feel free to add it... |
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
