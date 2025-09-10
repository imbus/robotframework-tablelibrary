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

        self.header:bool = True

    @property
    def file_reader(self):
        return FileReader(self.library, FileSync)

    @property
    def _fs(self):
        return FileSystem()

    def write_table(self,
                    data: DataFrame | list[list[Any]],
                    file_path: str | None = None
                    ) -> str:
        """Keyword to create/overwrite table using dataframe tables."""
        if file_path is None:
            file_path = self.file_reader.opened_table

        dir_name = Path(file_path).parent
        self._fs.ensure_directory_exists(dir_name)
        self.file_type = self.file_reader.read_data_type(file_path)

        if isinstance(data, list) and self.file_type == FileType.Parquet:
            data_df = pd.DataFrame(data[1:], columns=data[0])
        elif isinstance(data, list) and self.file_type != FileType.Parquet:
            data_df = pd.DataFrame(data)
        else:
            data_df = data

        #lists or 'headless' dataframes automatically add index in to_csv
        csv_header = self.header and not isinstance(data, list)

        writers = {
            FileType.CSV: lambda: data_df.to_csv(file_path, index=False, header=csv_header, sep=self.separator.value),
            # FileType.Excel: lambda: data_df.to_excel(file_path, index=False),
            FileType.Parquet: lambda: data_df.to_parquet(file_path)
        }

        writer = writers.get(self.file_type)
        if writer:
            writer()
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
        return file_path

    def write_table_file_cells(self,
                    data: Any,
                    row: None | int = None,
                    column: None | str | int = None,
                    file_path: None | str  = None,
                    header: bool = True,
                    ) -> str:
        """Keyword to manipulate data.
           data = if it is a list it can change complete row/column if the size
           of data matches the lenght of row/column.
           row = using for index of the row where in the table the cell should be manipulated.
                 If it is None then it will be all rows.
           column = Using for index/column name of the columns where in the table the cell should be manipulated.
                    If it is None then it will be all columns.
           header = if it is True then the header during manipulation will be included. Meaning index 0 will be manipulated.
                    If it is False then the 1st index will be treated as 0 index.
           file_path = Path where the table is located which should be manipulated. If it is None then it searches for 'read_table'."""

        table_df: DataFrame = {}
        table_df = self.file_reader.read_table_file(
            path = file_path if file_path is not None
                   else self.file_reader.opened_table)

        original_ignore_header = self.ignore_header

        # disable header for Parquet and overwrite ignore_header for validation keywords
        self.header = header if self.file_type != FileType.Parquet else False
        self.ignore_header = not self.header

        if self.header:
            headers = table_df.iloc[0].tolist()
            rows = table_df.iloc[1:]
            table_df = pd.DataFrame(rows.values, columns=headers)

        if isinstance(data, list):
            self.file_reader.validate_data_list_with_table(
                data=data,
                table=table_df,
                row=row,
                column=column,
            )

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
            file_path
        )

        self.ignore_header = original_ignore_header

        return self.file_sync.current_file
