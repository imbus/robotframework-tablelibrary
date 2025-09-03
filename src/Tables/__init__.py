# SPDX-FileCopyrightText: 2025-present Marvin Klerx <marvinklerx20@gmail.com>
#
# SPDX-License-Identifier: MIT
from .__about__ import __version__

from robot.api.deco import library
from robotlibcore import HybridCore

from .utils.settings import FileType, Delimiter, FileEncoding

from .keywords import (
    Configuration,
    Getter,
    Writer,
    Excel
)

@library(
    scope='GLOBAL',
    version=__version__
)
class Tables(HybridCore):
    """
    Table Library is a generic automation library for working with files like csv, parquet, etc.

    == Table of content ==

    %TOC%

    == Supported File Types ==
    - CSV
    - Excel (not supported at the moment)
    - Parquet

    == Supported File Encoding ==
    - utf-8
    - utf-16
    - latin-1

    == Excel Files ==
    Please visit the following to handle excel files: [https://pypi.org/project/robotframework-excelsage|robotframework-sageexcel]

    == Examples ==
    === CSV ===
    | # Reading CSV file with header column
    | ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    | ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "index"
    | BuiltIn.Should Be True    ${result}
    |
    |
    | # Reading CSV file without header column
    | Tables.Configure Ignore Header    True
    | ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    | ${result} =    BuiltIn.Evaluate    "index" not in "${content}"
    | BuiltIn.Should Be True    ${result}

    === Parquet ===
    | Tables.Configure File Type    Parquet
    | ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_05.parquet
    | ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "_time"
    | BuiltIn.Should Be True    ${result}
    """

    def __init__(
            self,
            *_,
            file_type: FileType = FileType.CSV,
            file_encoding: FileEncoding = FileEncoding.UTF8,
            delimiter: Delimiter = Delimiter[","],
            ignore_header: bool = False
        ):
        """
        Table Library can be controlled by the following arguments:

        | =`Argument`=      | =`Description`= |
        | ``file_type``     | Choose the file type to test initially. |
        | ``file_encoding`` | Defiine the file encoding. |
        | ``delimiter``     | Define a delimiter for parsing the files. |
        | ``ignore_header`` | Define if headers in files should be ignored. Default is ``False``  |
        """
        self._file_type = file_type
        self._delimiter = delimiter
        self._file_encoding = file_encoding
        self._ignore_header = ignore_header

        libraries = [
            Configuration(self),
            Getter(self),
            Writer(self),
            Excel(self)
        ]

        super().__init__(libraries)
