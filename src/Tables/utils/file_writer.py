from ..general.library_attributes import LibraryAttributes
from .file_reader import FileReader
from ..utils.settings import FileType
from ..utils.file_system import FileSystem, FileSync

from pathlib import Path
import pandas as pd
from pandas import DataFrame
from typing import Any

class FileWriter(LibraryAttributes):
    def __init__(self, library, file_sync: FileSync):
        super().__init__(library)
        self.file_sync = file_sync

    @property
    def file_reader(self):
        return FileReader(self.library, FileSync)

    @property
    def _fs(self):
        return FileSystem()

    def write_table(self,
                    data: DataFrame | list[list[Any]],
                    file_path: str | None = None):
        """"""
        if file_path is None:
            file_path = self.file_reader.opened_table

        data_df = data if isinstance(data, DataFrame) else pd.DataFrame(data)

        dir_name = Path(file_path).parent
        self._fs.ensure_directory_exists(dir_name)

        csv_header = not isinstance(data, list) #lists automatically add index in to_csv compared to dataframe

        writers = {
            FileType.CSV: lambda: data_df.to_csv(file_path, index=False, header=csv_header),
            FileType.Excel: lambda: data_df.to_excel(file_path, index=False),
            FileType.Parquet: lambda: data_df.to_parquet(file_path, index=False)
        }

        writer = writers.get(self.file_type)
        if writer:
            writer()
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
        return file_path



    def write_table_file_cell(self,
                    data: Any,
                    row: None | int = None,
                    column: None | str | int = None,
                    file_path: None | str  = None,
                    ) -> str:
        """"""
        table_df: DataFrame = {}

        table_df = self.file_reader.read_table_file(
            path = file_path if file_path is not None
                   else self.file_reader.opened_table)

        if isinstance(data, list) and len(data) != table_df.shape[1]:
            size_difference = "big" if len(data) > table_df.shape[1] else "small"
            raise ValueError(
                f"Selected list is too {size_difference} for the table ({len(data)}). "
                f"The size of the table is: {table_df.shape[0]} rows and  {table_df.shape[1]} columns."
            )

        headers = table_df.iloc[0].tolist()
        rows = table_df.iloc[1:]
        table_df = pd.DataFrame(rows.values, columns=headers)

        axis_row = row if row is not None else slice(None)
        axis_column = self.file_reader.cast_column_type(column) if column is not None else slice(None)

        if column:
            self.file_reader.validate_column(table_df, axis_column)
        if row:
            self.file_reader.validate_row(table_df, axis_row)

        if isinstance(axis_column, str):
            table_df.loc[axis_row, axis_column] = data
        else:
            table_df.iloc[axis_row, axis_column] = data

        self.write_table(
            table_df,
            self.file_sync.current_file
        )

        return self.file_sync.current_file
