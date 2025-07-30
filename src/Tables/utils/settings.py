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
    Predefined delimiters to use within the library.
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
