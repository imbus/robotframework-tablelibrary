from ..general.library_attributes import LibraryAttributes
from ..utils.settings import FileType
from ..utils.file_system import FileSync

import pandas as pd
from pandas import DataFrame
from pathlib import Path
from typing import cast, Any
from enum import Enum

class Axis(Enum):
            Columns = "columns"
            Rows = "rows"

class FileReader(LibraryAttributes):
    def __init__(self, library, file_sync: FileSync):
        super().__init__(library)
        self.file_sync = file_sync

    @property
    def opened_table(self)-> str:
        if not self.file_sync.current_file:
            raise ValueError(
                "No file open - use `Read Table` to read a file first!"
            )
        return self.file_sync.current_file

    def file_exists(self,
                    path: str
        ) -> bool | FileNotFoundError:
        if not Path(path).is_file():
            raise FileNotFoundError(f"File not found: {path}")
        return True

    def read_data_type(self,
                       path:str
        ) -> FileType:
        """
        Converts the file types depending on the ending of the filename
        """
        data_type = None
        if path.endswith(".csv"):
            data_type = FileType.CSV
        elif path.endswith(".parquet"):
            data_type = FileType.Parquet
        # elif path.endswith(".xlsx"):
        #     data_type = FileType.Excel
        else:
            raise TypeError(f"Invalid file type of {Path(path).name}. Allowed files are {[file_type.value for file_type in FileType]}")

        return data_type

    def cast_column_type(self,
                         column_value: int | str
        ) -> int | str:
        """
        Converts the value into int first (if possible) then to string. This way indexing and column names
        are stricktly sperated for further process.
        """
        try:
            return int(column_value)
        except (ValueError, TypeError):
            return str(column_value)


    def validate_column(self,
                        data: DataFrame,
                        column_value: int | str
        ) -> bool:
        """
        1) Validates whether the column value which should be extracted is int (index) or str(name of the column).
        Str type should only work if header is involed (!= ignore_header).
        2) Checks if column index is out of bound of the table.
        3) Checks if the column name is inside the table columns (only if != ignore header).
        """
        column_value = self.cast_column_type(column_value)

        if isinstance(column_value, str):
            if self.ignore_header:
                raise TypeError(
                    "Column identifier cannot be 'str' type when library setting 'ignore_header' is 'True'!"
                )
            if column_value not in data.iloc[0].tolist() and column_value not in data.columns:
                raise ValueError(
                    f"Couldn't find column '{column_value}' in the table. "
                    f"Current columns are: {list(data.iloc[0])}"
                )

        elif isinstance(column_value, int):
            if column_value + 1 > data.shape[1]:
                raise IndexError(
                    f"Selected column is out of bounds. The size of the table is: "
                    f"{data.shape[1]} columns."
                )

        return True

    def validate_row(self,
                    data: DataFrame,
                    row_value: int | list[Any]
        ) -> bool:
        """
        Validates whether the row is out of bound.
        """
        if isinstance(row_value, int) and row_value + 1 > data.shape[0]:
            raise IndexError(
                    f"Selected row is out of bounds. The size of the table is: {data.shape[0]} rows."
                )
        return True

    def validate_data_list_with_table(self,
                                       data: list,
                                       table: DataFrame,
                                       row: Any | None = None,
                                       column: Any | None = None,
                                       ):
        """
        Reads the data(as list) and compares it with the provided table (as dataframe). It checks if rows or column size matches the one of the table.
        Returns an error if both rows and columns are not None.
        data: Provided list whose size (len) should be checked.
        table: the table which should be compared against. Depending if 'column' or 'row' parameters are not None, this axis would be checked.
        row: If not None the row size of the table will be checked.
        column: If not None the column size of the table will be checked.
        """
        if row is not None and column is not None:
            raise ValueError("Cannot select both row and column if selected data is a list for manipulation.")

        selected_axis = 1 if row is not None else 0
        if len(data) != table.shape[selected_axis]:
            size_difference = "big" if len(data) > table.shape[selected_axis] else "small"
            raise ValueError(
                f"Selected list is too {size_difference} for the table ({len(data)}). "
                f"The size of the table is: {table.shape[0]} rows and  {table.shape[1]} columns."
            )
        return True


    def read_csv(self,
                 path: str
        ) -> DataFrame:
        """
        Opening up the csv file using and returning pandas dataframe.
        """
        return pd.read_csv(path,
                         sep=self.separator.value,
                         encoding=self.file_encoding.value,
                         header=None)

    def validate_table_to_dataframe(self,
                                    data: list[list[Any]],
                                    row: None | int = None,
                                    column: None | str | int = None,
                                    ) -> DataFrame:
        """Formats an already read table to dataframe. Also checks
        if provided row or column are valid (see validate_row/ validate_column)."""
        df = DataFrame(data)

        if row:
            self.validate_row(df, row)

        if column:
            casted_column = self.cast_column_type(column)
            self.validate_column(df, casted_column)
            if isinstance(casted_column, str):
                df = DataFrame(data[1:], columns=data[0])
        return df



    def read_excel(self,
                   path: str,
                   sheet_name: str | list[str | int] | None = None
        ) -> dict[str, DataFrame]:
        header = 0 if self.ignore_header else None
        dict_df = pd.read_excel(path, header=header, sheet_name=sheet_name)
        return {sheet_name: dict_df} if isinstance(sheet_name, str) else cast(dict[str, DataFrame], dict_df)

    def read_parquet(self, path:str) -> DataFrame:
        """
        """
        return pd.read_parquet(path)

    def read_table_file(self,
                        path: str
                        ) -> DataFrame:
        """
        Reading table file and returns a dataframe of it.
        """
        table_df: DataFrame = {}
        self.file_exists(path)

        self.file_sync.current_file = path

        self.file_type = self.read_data_type(path)

        if self.file_type == FileType.CSV:
            table_df = self.read_csv(path)

        elif self.file_type == FileType.Parquet:
            table_df = self.read_parquet(path)

        else:
            raise ValueError(f"Not supported data type - file path: {path}")

        return table_df
