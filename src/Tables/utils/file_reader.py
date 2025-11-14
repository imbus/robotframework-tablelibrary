from enum import Enum
from pathlib import Path
from typing import Any, cast

import pandas as pd
from pandas import DataFrame
from robot.api import logger

from ..general.library_attributes import LibraryAttributes
from ..utils.file_system import FileSync, TableObject
from ..utils.settings import FileSuffix, FileType, TableFormat


class Axis(Enum):
    Columns = "columns"
    Rows = "rows"


class FileReader(LibraryAttributes):
    def __init__(self, library, file_sync: FileSync):
        super().__init__(library)
        self.file_sync = file_sync

    @property
    def opened_table_path(self) -> Path:
        if self.file_sync.current_file is None:
            raise ValueError("No file path found - use `Open Table` to read a file first!")
        return self.file_sync.table_storage[self.file_sync.current_file].path

    @property
    def current_alias(self) -> str:
        if self.file_sync.current_file is None:
            raise ValueError("No file open - use `Open Table` to read a file first!")
        return self.file_sync.current_file

    def convert_dataframe(
        self, data: DataFrame, return_type: TableFormat = TableFormat["List of lists"]
    ) -> list[list] | list[dict] | DataFrame:
        """"""
        if return_type == TableFormat["List of lists"]:
            list_data = cast(list[list], data.values.tolist())

            if self.file_type == FileType.Parquet and not self.ignore_header:
                list_data.insert(0, list(data.columns))

            return list_data
        if return_type == TableFormat["List of dicts"]:
            df_for_dicts = data

            if self.file_type != FileType.Parquet and not self.ignore_header and not data.empty:
                header = [str(x) for x in df_for_dicts.iloc[0].tolist()]
                df_for_dicts = df_for_dicts.iloc[1:].copy()
                df_for_dicts.columns = header
            return cast(list[dict[str, Any]], df_for_dicts.to_dict(orient="records"))
        if return_type == TableFormat["Dataframe"]:
            return data
        raise ValueError(
            f"Invalid TableFormat type. Please select valid values: {[key.name for key in TableFormat]}"
        )

    def file_exists(self, path: Path) -> bool | FileNotFoundError:
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")
        return True

    def check_default_dataframe_header(self, table: DataFrame) -> bool:
        """Checks if Dataframe has default index ([0,1,2,3..]) and if it does returns True. If it detects unique columns returns False."""
        table_column_count = table.shape[1]
        default_index = [str(i) for i in range(table_column_count)]
        table_header = [str(i) for i in table.columns.to_list()]

        # Compare the two lists
        return table_header == default_index

    def reset_header_dataframe(self, table: DataFrame) -> DataFrame:
        """Checks if Dataframe has default index ([0,1,2,3..]) and if it does the Dataframe remains the same. If it detects unique columns
        it puts them into the body of dataframe and makes the header as basic index.
        Parquet is special case since the default header is not index based but with unique columns. Thus it will not have index as headers."""
        table_header = table.columns.to_list()
        table_data = table.values.tolist()

        if self.file_type == FileType.Parquet:
            if not self.check_default_dataframe_header(table):
                return table
            header = table.iloc[0].tolist()
            data = table[1:].values
            return DataFrame(data, columns=header)
        if self.check_default_dataframe_header(table):
            return table
        header_data_table = [table_header]
        header_data_table.extend(table_data)
        return DataFrame(header_data_table, columns=None)

    def read_data_type(self, path: Path) -> FileType:
        """
        Converts the file types depending on the ending of the filename
        """
        if FileSuffix.CSV.value in path.suffix or FileSuffix.TXT.value in path.suffix:
            return FileType.CSV
        if FileSuffix.XLSX.value in path.suffix or FileSuffix.XLS.value in path.suffix:
            return FileType.Excel
        if FileSuffix.Parquet.value in path.suffix:
            return FileType.Parquet
        raise TypeError(
            f"Invalid file type of {Path(path).name}. Allowed files are {[file_type.value for file_type in FileType]}"
        )

    def cast_column_type(self, column_value: int | str) -> int | str:
        """
        Converts the value into int first (if possible) then to string. This way indexing and column names
        are stricktly sperated for further process.
        """
        try:
            return int(column_value)
        except (ValueError, TypeError):
            return str(column_value)

    def cast_path_type(self, path: Path | str) -> str | Path:
        if isinstance(path, Path):
            return path

        valid_path = Path(path)
        if valid_path.exists():
            return valid_path
        return path

    def validate_column(self, data: DataFrame, column_value: int | str) -> bool:
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
                    f"Couldn't find column '{column_value}' in the table. Current columns are: {list(data.iloc[0])}"
                )

        elif isinstance(column_value, int):
            if column_value + 1 > data.shape[1]:
                raise IndexError(
                    f"Selected column is out of bounds. The size of the table is: {data.shape[1]} columns."
                )

        return True

    def validate_row(self, data: DataFrame, row_value: int | list[Any]) -> bool:
        """
        Validates whether the row is out of bound.
        """
        if isinstance(row_value, int) and row_value + 1 > data.shape[0]:
            raise IndexError(
                f"Selected row is out of bounds. The size of the table is: {data.shape[0]} rows."
            )
        return True

    def validate_data_list_with_table(
        self, data: list, table: DataFrame, row: Any | None = None, column: Any | None = None
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
            raise ValueError(
                "Cannot select both row and column if selected data is a list for manipulation."
            )
        if row is None and column is None:
            raise ValueError(
                "Cannot ignore both row and column if selected data is a list for manipulation."
            )

        selected_axis = 1 if row is not None else 0
        if len(data) != table.shape[selected_axis]:
            size_difference = "big" if len(data) > table.shape[selected_axis] else "small"
            raise ValueError(
                f"Selected list is too {size_difference} for the table ({len(data)}). "
                f"The size of the table is: {table.shape[0]} rows and  {table.shape[1]} columns."
            )
        return True

    def read_csv(self, path: Path) -> DataFrame:
        """
        Opening up the csv file using and returning pandas dataframe.
        """
        return pd.read_csv(
            path,
            sep=self.separator.value,
            encoding=self.file_encoding,
            header=None,
            # lineterminator="\r\n"  #TODO:the culprit for weird readings and writings of table
        )

    def validate_table_to_dataframe(
        self,
        data: list[list] | DataFrame,
        row: None | int = None,
        column: None | str | int = None,
    ) -> DataFrame:
        """Formats a table (list of lists or dataframe) to dataframe. Also checks
        if provided row or column are valid (see validate_row/ validate_column)."""
        if isinstance(data, list):
            data = DataFrame(data)

        if row:
            self.validate_row(data, row)

        if column:
            column = self.cast_column_type(column)
            self.validate_column(data, column)

        if self.file_type != FileType.Parquet and (isinstance(column, str) or self.ignore_header):
            data.columns = data.iloc[0].to_list()
            data = data[1:].reset_index(drop=True)
        return data

    def read_excel(self, path: Path, **kwargs) -> DataFrame:
        return pd.read_excel(path, header=None, sheet_name=kwargs.get("sheet_name", 0))

    def read_parquet(self, path: Path) -> DataFrame:
        """ """
        df: DataFrame = pd.read_parquet(path)

        # try to transform to ISO timeformat -> if transformation fails, just return original parquet dataframe
        try:
            return self._parquet_transform_to_iso_timeformat(df)
        except Exception:
            return pd.read_parquet(path)

    def _parquet_transform_to_iso_timeformat(self, df: DataFrame) -> DataFrame:
        ts_cols = df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns
        for col in ts_cols:
            df[col] = df[col].dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            df[col] = df[col].str[:-3] + "Z"
        return df

    def read_table_file(self, path: Path) -> DataFrame:
        """
        Reading table file and returns a dataframe (without header settings) of it.
        """
        table_df: DataFrame = {}

        if path is not None:
            self.file_exists(path)
            readers = {
                FileType.CSV: lambda: self.read_csv(path),
                FileType.Excel: lambda: self.read_excel(path),
                FileType.Parquet: lambda: self.read_parquet(path),
            }
            self.file_type = self.read_data_type(path)

            reader = readers.get(self.file_type)
            if reader:
                table_df = reader()
            else:
                raise ValueError(f"Not supported data type - file path: {path}")

        return table_df

    def open_table_dataframe(self, alias: str, path: Path) -> str:
        """
        Reads a file and puts it in table_storage as cached table with path.
        """
        self.file_exists(path)

        _df = self.read_table_file(path=path)

        self.file_sync.current_file = alias
        self.file_sync.table_storage[self.file_sync.current_file] = TableObject(path, _df)

        return self.file_sync.current_file

    def create_empty_table_dataframe(self, alias: str, headers: list):
        df = pd.DataFrame(columns=headers)

        self.file_sync.current_file = alias
        self.file_sync.table_storage[self.file_sync.current_file] = TableObject(Path("unknown"), df)

        return self.file_sync.current_file

    def close_table_dataframe(self, alias: str | None = None) -> bool:
        """"""
        if not self.file_sync.table_storage:
            logger.info("Nothing to close - no file is opened!")
            return False
        if not alias:
            self.file_sync.table_storage = {}
            self.file_sync.current_file = None
            logger.info("Closed all opened files!")
            return True
        if alias in self.file_sync.table_storage:
            del self.file_sync.table_storage[alias]
            if len(self.file_sync.table_storage) == 0:
                self.file_sync.current_file = None
            logger.info(f"Selected file '{alias}' is closed!")
            return True
        raise KeyError(
            f"Given file alias '{alias}' does not exist - check all opened files and their alias first!"
        )

    def table_dataframe_switch(self, alias: str) -> str:
        """
        Keyword to switch between opened excel files - only if more than one file is opened.

        | =`Arguments`= | =`Description`= |
        | ``alias`` | The defined ``alias`` of the file to switch to. |

        == Example ==
        | Excel File Switch    file_a
        | Excel File Switch    file_b
        """
        if len(self.file_sync.table_storage) <= 1:
            raise KeyError(
                "No or only one file is opened at the moment - please open at least two files to use this keyword!"
            )
        self.file_sync.current_file = alias
        return self.file_sync.current_file
