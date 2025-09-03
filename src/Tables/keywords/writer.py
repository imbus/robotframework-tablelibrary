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
            column: int,
            header: bool = True,
            file_path: str | None = None,
        ) -> list[list[Any]]:
        """
        Keyword to (over-) write the value of a specific cell.
        """
        self.file_writer.write_table_file_cells(
            data = data,
            row = row,
            column = column,
            header= header,
            file_path = file_path
        )

        return [[None]]

    @keyword(tags=["Writer"])
    def write_table_column(
            self,
            data: list[Any],
            column: int,
            header: bool = True,
            file_path: str | None = None,
        ) -> list[list[Any]]:

        self.file_writer.write_table_file_cells(
            data = data,
            column = column,
            header= header,
            file_path = file_path
        )

        return [[None]]

    @keyword(tags=["Writer"])
    def write_table_row(
            self,
            data: list,
            row: int,
            header: bool = True,
            file_path: str | None = None,
        ) -> list[list[Any]]:

        self.file_writer.write_table_file_cells(
            data = data,
            row = row,
            header= header,
            file_path = file_path
        )

        return [[None]]
