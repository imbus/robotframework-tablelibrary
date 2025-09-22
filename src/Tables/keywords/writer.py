from robot.api.deco import keyword
from ..general.library_attributes import LibraryAttributes
from ..utils.settings import FileType, TableFormat
from ..utils.file_system import FileSystem
from ..utils.file_access import FileAccess

from pathlib import Path


class Writer(LibraryAttributes):

    def __init__(self, library, file_access:FileAccess):
        self.library = library
        self.file_writer = file_access.file_writer

    @property
    def _fs(self):
        return FileSystem()

    @keyword(tags=['Writer'])
    def write_table(
            self,
            data: list[list],
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
    def set_table_cell(
            self,
            data: str,
            row: int,
            column: int | str,
            header: bool = True,
        ) -> list[list]:
        """
        Keyword to (over-) write the value of a specific cell.

        | =`Arguments`= | =`Description`= |
        | ``data`` | The new value for the given table cell. |
        | ``row`` | Define the index of the row to identify the cell. |
        | ``column`` | Define the index of the column to identify the cell. Is column is a string then header should be set on True.|
        | ``header`` | Set to ``True`` if header should be recognized during file modifications - if ``False`, its ignored. |
        | ``file_path`` | The full path of the existing table file. |

        == Example ==
        |  Set Table Cell    New York    row=20    column=2    file_path=${CURDIR}/output/statistics.csv    header=False
        |  Set Table Cell    Apple    row=1    column=Fruit    file_path=${CURDIR}/output/statistics.csv    header=True   #per default it is true
        """
        original_ignore_header = self.ignore_header

        # disable header for Parquet and overwrite ignore_header for validation keywords
        self.file_writer.header = header if self.file_type != FileType.Parquet else False
        self.ignore_header = not self.file_writer.header

        table_df:list[list] = self.file_writer.set_dataframe_cells(
            data = data,
            row = row,
            column = column,
            return_type=TableFormat["List of lists"]
        )

        self.ignore_header = original_ignore_header
        return table_df

    @keyword(tags=["Writer"])
    def set_table_column(
            self,
            data: list,
            column: int,
            header: bool = True,
        ) -> list[list]:
        """
        Keyword to (over-) write the values of a specific column.

        | =`Arguments`= | =`Description`= |
        | ``data`` | The new values for the given table column - needs to be list object. |
        | ``column`` | Define the index of the column to modify. |
        | ``header`` | Set to ``True`` if header should be recognized during file modifications - if ``False`, its ignored. |
        | ``file_path`` | The full path of the existing table file. |

        == Example ==
        |  VAR   @{column_list}    month    august    march
        |  Set Table Column    ${column_list}    2    ${CURDIR}/output/statistics.csv    True
        """

        self.file_writer.set_dataframe_cells(
            data=data,
            column = column,
            header= header,
        )

        return [[None]]

    @keyword(tags=["Writer"])
    def set_table_row(
            self,
            data: list,
            row: int,
            header: bool = True,
        ) -> list[list]:
        """
        Keyword to (over-) write the values of a specific row.

        | =`Arguments`= | =`Description`= |
        | ``data`` | The new values for the given table row - needs to be list object. |
        | ``row`` | Define the index of the row to modify. |
        | ``header`` | Set to ``True`` if header should be recognized during file modifications - if ``False`, its ignored.
        |              If Header = False and row index = 0 it will overwrite a possible header, if there is one!|
        | ``file_path`` | The full path of the existing table file. |

        == Example ==
        |  Set Table Row    ${list_of_values}    3    ${CURDIR}/output/statistics.csv    True
        """

        self.file_writer.set_dataframe_cells(
            data=data,
            row = row,
            header= header,
        )

        return [[None]]
