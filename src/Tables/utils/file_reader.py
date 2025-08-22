from ..general.library_attributes import LibraryAttributes
from ..utils.settings import FileType

import pandas as pd
from pandas import DataFrame
from pathlib import Path
from typing import cast
from enum import Enum

class Axis(Enum):
            Columns = "columns"
            Rows = "rows"

class FileReader(LibraryAttributes):
    def __init__(self, library):
        super().__init__(library)

    def file_exists(self, path: str) -> bool | FileNotFoundError:
        if not Path(path).is_file():
            raise FileNotFoundError(f"File not found: {path}")
        return True

    def read_data_type(self, path:str) -> FileType:
        """
        Converts the file types depending on the ending of the filename
        """
        data_type = None
        if path.endswith(".csv"):
            data_type = FileType.CSV
        elif path.endswith(".parquet"):
            data_type = FileType.Parquet
        else:
            raise TypeError(f"Invalid file type of {Path(path).name}. Allowed files are {[file_type.value for file_type in FileType]}")

        return data_type

    def cast_column_type(self, column_value: int | str) -> int | str:
        """
        Converts the value into int first (if possible) then to string. This way indexing and column names
        are stricktly sperated for further process.
        """
        try:
            return int(column_value)
        except (ValueError, TypeError):
            return str(column_value)


    def validate_column(self, data: DataFrame, column_value: int | str) -> bool:
        """
        1) Validates whether the column value which should be extracted is int (index) or str(name of the column).
        Str type should only work if header is involed (!= ignore_header).
        2) Checks if column index is out of bound of the table.
        3) Checks if the column name is inside the table columns (only if != ignore header).
        """
        column_value = self.cast_column_type(column_value)

        if self.ignore_header and isinstance(column_value, str):
            raise TypeError(
                "Column identifier cannot be 'str' type, when library setting 'ignore_header' is 'True'!"
            )
        if isinstance(column_value, int) and column_value + 1 > data.shape[1]:
            raise IndexError(
                f"Selected column is out of bounds. The size of the table is: {data.shape[1]} columns."
            )
        if not self.ignore_header and \
            isinstance(column_value, str) and \
            column_value not in list(data.iloc[0]):
            raise ValueError(f"Couldn't find column {column_value} in the table. Current columns are: {list(data.iloc[0])}")
        return True

    def validate_row(self, data: DataFrame, row_value: int) -> bool:
        """
        Validates whether the row is out of bound.
        """
        if row_value + 1 > data.shape[0]:
            raise IndexError(
                f"Selected row is out of bounds. The size of the table is: {data.shape[0]} columns."
            )
        return True

    def read_csv(self, path: str) -> DataFrame:
        """
        """
        return pd.read_csv(path,
                         sep=self.delimiter.value,
                         encoding=self.file_encoding.value,
                         header=None)

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
        Reading table
        """
        table_df: DataFrame = {}
        self.file_exists(path)

        read_type = self.read_data_type(path)
        self.file_type = read_type

        if self.file_type == FileType.CSV:
            table_df = self.read_csv(path)

        elif self.file_type == FileType.Parquet:
            table_df = self.read_parquet(path)

        else:
            raise ValueError(f"Not supported data type - file path: {path}")

        if self.ignore_header and self.file_type != FileType.Parquet:
                table_df = table_df.iloc[1:]
        return table_df
