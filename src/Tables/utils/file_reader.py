from ..general.library_attributes import LibraryAttributes
from ..utils.settings import FileType

import pandas as pd
from pandas import DataFrame
from pathlib import Path
from typing import cast


class FileReader(LibraryAttributes):
    def __init__(self, library):
        super().__init__(library)

    def file_exists(self, path: str) -> bool | FileNotFoundError:
        if not Path(path).is_file():
            raise FileNotFoundError(f"File not found: {path}")
        return True

    def read_data_type(self, path:str) -> FileType:
        data_type = None
        if path.endswith(".csv"):
            data_type = FileType.CSV
        elif path.endswith(".parquet"):
            data_type = FileType.Parquet
        else:
            raise TypeError(f"Invalid file type of {Path(path).name}. Allowed files are {[file_type.value for file_type in FileType]}")

        return data_type


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

        if self.ignore_header:
                table_df = table_df.iloc[1:]
        return table_df






