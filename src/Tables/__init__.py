# SPDX-FileCopyrightText: 2025-present Marvin Klerx <marvinklerx20@gmail.com>
#
# SPDX-License-Identifier: MIT
from .__about__ import __version__

from robot.api.deco import library
from robotlibcore import HybridCore

from .utils.settings import FileType, Delimiter, FileEncoding

from .keywords import (
    Configuration,
    Getter
)

@library(
    scope='GLOBAL',
    version=__version__
)
class Tables(HybridCore):
    """
    Table Library is a generic automation library for working with file types like csv, excel, etc.

    == Table of content ==

    %TOC%

    === Supported file types ===
    | CSV     | Classic CSV file   |
    | Excel   | Classic Excel file |
    | Parquet | Parquet file       |
    """
    
    def __init__(
            self,
            *_,
            file_type: FileType,
            file_encoding: FileEncoding = FileEncoding.UTF8,
            delimiter: Delimiter = Delimiter[";"],
            ignore_header: bool = False
        ):
        """
        Table Library can be controlled by the following arguments:

        | =`Argument`=      | =Description= |
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
            Getter(self)
        ]

        super().__init__(libraries)