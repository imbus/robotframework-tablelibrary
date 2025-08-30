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
        if not file_path:
            file_path = self.file_reader.opened_table

        if not isinstance(data, DataFrame):
            data = pd.DataFrame(data)

        dir_name = Path(file_path).parent
        self._fs.ensure_directory_exists(dir_name)

        if not self.ignore_header:
            headers = data.iloc[0].tolist()
            rows = data.iloc[1:]
            df = pd.DataFrame(rows.values, columns=headers)
        else:
            df = pd.DataFrame(data)

        writers = {
            FileType.CSV: lambda: df.to_csv(file_path, index=False),
            FileType.Excel: lambda: df.to_excel(file_path, index=False),
            FileType.Parquet: lambda: df.to_parquet(file_path, index=False)
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
                    ) -> str:
        """"""
        # TODO: add path to skip current file
        table_df: DataFrame = {}
        if self.file_reader.opened_table:
            table_df = self.file_reader.read_table_file(self.file_reader.opened_table)

        axis_row = row if row else slice(None)
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
