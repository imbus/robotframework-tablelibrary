from robot.api.deco import keyword
from ..general.library_attributes import LibraryAttributes
from ..utils.file_system import FileSystem
from ..utils.file_writer import FileWriter
from ..utils.file_system import FileSync
from pathlib import Path

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
            file_path: Path
        ) -> str:
        """
        Keyword to write the given data to a new file or overwrite an existing file.

        | =`Arguments`= | =`Description`= |
        | ``data`` | Data object to store in a new file |
        | ``file_path`` | The full path of the table file to save the content in. |

        == Data Object ==
        The given data object with the argument ``data`` needs to be a list of lists to replicate the table structure

        == Example ==
        | Write Table    ${data}    ${CURDIR}/output/statistics.csv
        """
        self.file_writer.write_table(
            data,
            file_path
        )
        return str(file_path)

    @keyword(tags=["Writer"])
    def write_table_cell(
            self,
            data: str,
            row: int,
            column: int | str,
            file_path: Path | None = None,
            header: bool = True,
        ) -> list[list[Any]]:
        """
        Keyword to (over-) write the value of a specific cell.

        | =`Arguments`= | =`Description`= |
        | ``data`` | The new value for the given table cell. |
        | ``row`` | Define the index of the row to identify the cell. |
        | ``column`` | Define the index of the column to identify the cell. Is column is a string then header should be set on True.|
        | ``header`` | Set to ``True`` if header should be recognized during file modifications - if ``False`, its ignored. |
        | ``file_path`` | The full path of the existing table file. |

        == Example ==
        |  Write Table Cell    New York    row=20    column=2    file_path=${CURDIR}/output/statistics.csv    header=False
        |  Write Table Cell    Apple    row=1    column=Fruit    file_path=${CURDIR}/output/statistics.csv    header=True   #per default it is true
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
            file_path: Path | None = None,
            header: bool = True,
        ) -> list[list[Any]]:
        """
        Keyword to (over-) write the values of a specific column.

        | =`Arguments`= | =`Description`= |
        | ``data`` | The new values for the given table column - needs to be list object. |
        | ``column`` | Define the index of the column to modify. |
        | ``header`` | Set to ``True`` if header should be recognized during file modifications - if ``False`, its ignored. |
        | ``file_path`` | The full path of the existing table file. |

        == Example ==
        |  VAR   @{column_list}    month    august    march
        |  Write Table Column    ${column_list}    2    ${CURDIR}/output/statistics.csv    True
        """

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
            file_path: Path | None = None,
            header: bool = True,
        ) -> list[list[Any]]:
        """
        Keyword to (over-) write the values of a specific row.

        | =`Arguments`= | =`Description`= |
        | ``data`` | The new values for the given table row - needs to be list object. |
        | ``row`` | Define the index of the row to modify. |
        | ``header`` | Set to ``True`` if header should be recognized during file modifications - if ``False`, its ignored.
        |              If Header = False and row index = 0 it will overwrite a possible header, if there is one!|
        | ``file_path`` | The full path of the existing table file. |

        == Example ==
        |  Write Table Row    ${list_of_values}    3    ${CURDIR}/output/statistics.csv    True
        """

        self.file_writer.write_table_file_cells(
            data = data,
            row = row,
            header= header,
            file_path = file_path
        )

        return [[None]]
