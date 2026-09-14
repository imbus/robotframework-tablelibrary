from pathlib import Path

from robot.api.deco import keyword

from ..general.library_attributes import LibraryAttributes
from ..utils.file_access import FileAccess
from ..utils.file_system import FileSystem
from ..utils.settings import TableFormat


class Writer(LibraryAttributes):
    def __init__(self, library, file_access: FileAccess):
        self.library = library
        self.file_writer = file_access.file_writer
        self.file_reader = file_access.file_reader

    @property
    def _fs(self):
        return FileSystem()

    @keyword(tags=["Writer"])
    def write_table(self, data: list[list] | str, file_path: Path | str | None = None) -> str:
        """
        Keyword to write the given data to a new file or overwrite an existing file.

        Args:
            data: Data object to store in a new file.
            file_path: Full path of the table file to save the content in. If an alias from `Open Table` is used, the data is written to the alias file path. If no file path is selected, the current alias is used.

        ## Data Object
        The given data object with the argument ``data`` needs to be a list of lists to replicate the table structure

        Returns:
            Returns the path of written table as a string.

        ## Example
        ```robotframework
        *** Test Cases ***
        Write A Table
            Write Table    ${data}    statistics.csv
            Tables.Open Table    table 1    new_statistics.csv
            Tables.Write Table    ${data}    table 1
        ```
        """
        if isinstance(data, str):
            current_df = self.file_reader.file_sync.table_storage[self.file_reader.file_sync.current_file].data
            table_df = self.file_reader.validate_table_to_dataframe(data=current_df)
            data = self.file_reader.convert_dataframe(table_df)

        self.file_writer.write_table(data, file_path)

        return str(file_path)

    @keyword(tags=["Writer", "datastreaming"])
    def set_table_cell(
        self,
        data: str,
        row: int,
        column: int | str,
        header: bool = True,
    ) -> list[list]:
        """
        Keyword to (over-) write the value of a specific cell of the current table (see Open Table).

        Args:
            data: The new value for the given table cell.
            row: Define the index of the row to identify the cell.
            column: Define the index of the column to identify the cell. `header` must be `True` if the column is a string.
            header: Local override for the `ignore_header` logic.

        ## Example
        ```robotframework
        *** Test Cases ***
        Set A Table Cell
            Tables.Open Table    table 1    ${csv_path}
            Set Table Cell    New York    row=20    column=2    header=False
            Set Table Cell    Apple    row=1    column=Fruit    header=True
        ```
        """

        table_df: list[list] = self.file_writer.set_dataframe_cells(
            data=data,
            row=row,
            column=column,
            header=header,
            return_type=TableFormat["List of lists"],
        )
        return table_df

    @keyword(tags=["Writer", "datastreaming"])
    def set_table_column(
        self,
        data: list,
        column: int | str,
        header: bool = True,
    ) -> list[list]:
        """
        Keyword to (over-) write the values of a specific column.

        Args:
            data: The new values for the given table column. Must be a list.
            column: Define the index of the column to modify.
            header: Set to `True` if the header should be recognized. If `False`, it is ignored.

        ## Example
        ```robotframework
        *** Test Cases ***
        Set A Table Column
            VAR    @{column_list}    month    august    march
            Set Table Column    ${column_list}    2    header=True
        ```
        """
        table: list[list] = self.file_writer.set_dataframe_cells(
            data=data, column=column, header=header, return_type=TableFormat["List of lists"]
        )
        return table

    @keyword(tags=["Writer", "datastreaming"])
    def set_table_row(
        self,
        data: list,
        row: int,
        header: bool = True,
    ) -> list[list]:
        """
        Keyword to (over-) write the values of a specific row.

        Args:
            data: The new values for the given table row. Must be a list.
            row: Define the index of the row to modify.
            header: Define a local override for the `ignore_header` logic.

        ## Example
        ```robotframework
        *** Test Cases ***
        Set A Table Row
            Set Table Row    ${list_of_values}    3    header=True
        ```
        """
        table: list[list] = self.file_writer.set_dataframe_cells(
            data=data, row=row, header=header, return_type=TableFormat["List of lists"]
        )
        return table
