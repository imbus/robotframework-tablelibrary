# SPDX-FileCopyrightText: 2025-present Marvin Klerx <marvinklerx20@gmail.com>
#
# SPDX-License-Identifier: MIT
from typing import Union, Any, Optional
from overrides import overrides
from .__about__ import __version__

from robot.api.deco import library
from robotlibcore import DynamicCore

from .utils.data_types import FileType, Delimiter, FileEncoding

from .keywords import (
    Configuration
)

@library(
    scope='GLOBAL',
    version=__version__
)
class TableLibrary(DynamicCore):
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
            file_type: Union[FileType, Any],
            file_encoding: Union[FileEncoding] = FileEncoding.UTF8,
            delimiter: Union[Delimiter, Any] = Delimiter[";"],
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
            Configuration()
        ]

        super().__init__(libraries)

    @overrides
    def get_keyword_documentation(self, name):
        doc = DynamicCore.get_keyword_documentation(self, name)
        return doc