from robot.api.deco import keyword
from ..general.library_attributes import LibraryAttributes
from ..utils.file_system import FileSystem
from ..utils.file_writer import FileWriter
from ..utils.file_system import FileSync

from typing import Any

class Writer(LibraryAttributes):

    def __init__(self, library):
        self.library = library
        self.file_writer = FileWriter(library, FileSync)

    @property
    def _fs(self):
        return FileSystem()

    @keyword(tags=['Writer'])
    def write_table(
            self,
            data: list[list[Any]],
            file_path: str
        ) -> str:
        """
        Keyword to write the given data to a new file.

        | =`Arguments`= | =`Description`= |
        | ``data`` | Data object to store in a new file |
        | ``file_path`` | The full path of your file system to store the file. |

        == Example ==
        | Write Table    ${data}    ${CURDIR}/output/statistics.csv
        """
        self.file_writer.write_table(
            data,
            file_path
        )
        return file_path

    @keyword(tags=["Writer"])
    def write_table_cell(
            self,
            data: str,
            row: int,
            column: int
        ) -> list[list[Any]]:
        """
        Keyword to (over-) write the value of a specific cell.
        """
        self.file_writer.write_table_file_cell(
            data,
            row,
            column
        )

        return [[None]]

    @keyword(tags=["Writer"])
    def write_column(
            self,
            alias: str,
            column: int
        ) -> list[list[Any]]:
        return [[None]]

    @keyword(tags=["Writer"])
    def write_row(
            self,
            alias: str,
            row: int,
        ) -> list[list[Any]]:
        return [[None]]
