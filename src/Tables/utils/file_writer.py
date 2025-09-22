from ..general.library_attributes import LibraryAttributes
from .file_reader import FileReader
from ..utils.settings import FileType, TableFormat
from ..utils.file_system import FileSystem, FileSync

from pathlib import Path
import pandas as pd
from pandas import DataFrame
from typing import Any
from enum import Enum

class ModifyAction(Enum):
    Insert_Row = "insert row"
    Insert_Column = "insert column"
    Append_Row = "append row"
    Append_Column = "append column"
    Remove_Row = "remove row"
    Remove_Column = "remove column"

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

    @property
    def current_table(self):
        return self.file_sync.table_storage[self.file_sync.current_file]

    def insert_column_to_dataframe(self,
                                   column_index: int | str | None,
                                   column_data: list | None,
                                   table: DataFrame,
                                   ) -> DataFrame:
        if column_index is None or column_data is None:
            raise ValueError(f"Cannot insert column if either column index ({column_index})"
                             f"or column data ({column_data}) is empty.")

        self.file_reader.validate_data_list_with_table(
                data=column_data[1:] if self.header else column_data,
                table=table,
                column=column_index
            )
        table.insert(loc=column_index,
                        column=column_data[0] if self.header else column_index,
                        value=column_data[1:] if self.header else column_data
                        )
        return table

    def insert_row_to_dataframe(self,
                                row_index: int | None,
                                row_data: list | None,
                                table: DataFrame) -> DataFrame:
        if row_index is None or row_data is None:
            raise ValueError(f"Cannot insert row if either row index ({row_index})"
                             f"or row data ({row_data}) is empty.")
        self.file_reader.validate_data_list_with_table(
                data=row_data,
                table=table,
                row=row_index
            )
        data_df = DataFrame([row_data],
                            columns=table.columns.to_list() if self.header else None,
                            )

        return pd.concat(objs=[table[:row_index],
                                    data_df,
                                    table[row_index:]],
                                ignore_index=True)

    def append_column_to_dataframe(self,
                                   column_data: list | None,
                                   table: DataFrame) -> DataFrame:
        if column_data is None:
            raise ValueError(f"Cannot append column if column data({column_data}) is empty.")

        self.file_reader.validate_data_list_with_table(
                data=column_data[1:] if self.header else column_data,
                table=table,
                column=1
            )
        new_column_index = table.shape[1] + 1 if not self.header else column_data[0]
        new_column_data = column_data if not self.header else column_data[1:]
        table[new_column_index] = new_column_data

        return table

    def append_row_to_dataframe(self,
                                row_data : list | None,
                                table:DataFrame) -> DataFrame:
        if row_data is None:
            raise ValueError(f"Cannot append row if row data({row_data}) is empty.")

        self.file_reader.validate_data_list_with_table(
                data=row_data,
                table=table,
                row=1
            )
        data_df = DataFrame([row_data], columns=table.columns.to_list() if self.header else None)
        return pd.concat(objs=[table, data_df],
                          ignore_index=True)

    def remove_column_dataframe(self,
                                column_index: str | int | None,
                                table:DataFrame)-> DataFrame:
        if column_index is None:
            raise ValueError(f"Cannot remove column if column index({column_index}) is empty.")

        column_index = table.columns[column_index] if isinstance(column_index, int) else column_index
        return table.drop(column_index, axis=1)

    def remove_row_dataframe(self,
                             row_index: int | None,
                             table: DataFrame) -> DataFrame:
        if row_index is None:
            raise ValueError(f"Cannot remove row if row index({row_index}) is empty.")
        return table.drop(row_index)

    def write_table(self,
                    data: DataFrame | list[list],
                    file_path: Path | None = None
                    ) -> Path:
        """Keyword to create/overwrite table using dataframe tables."""
        if file_path is None:
            file_path = self.file_reader.opened_table_path

        dir_name = file_path.parent
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
            FileType.CSV: lambda: data_df.to_csv(file_path,
                                                 index=False,
                                                 header=csv_header,
                                                 #sep=self.separator.value,
                                                 #quoting=self.quoting.value,
                                                 #quotechar=self.quoting_character.value
                                                ),
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
                    file_path: Path | None  = None,
                    header: bool = True,
                    ) -> Path:
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

        table_df = self.file_reader.read_table_file(path = file_path)

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

        return file_path if file_path is not None else self.current_table.path

    def set_dataframe_cells(self,
                            data: Any,
                            row: None | int = None,
                            column: None | str | int = None,
                            header: bool = True,
                            return_type: TableFormat = TableFormat["Dataframe"]
        ) -> list[list] | list[dict] | DataFrame:
        """"""
        table_df = self.current_table.data

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

        self.ignore_header = original_ignore_header

        return self.file_reader.convert_dataframe(table_df, return_type)


    def modify_table(self,
                     action: ModifyAction,
                     data: list | None = None,
                     row: int | None = None,
                     column: str | int | None = None,
                     header: bool = True,
                     )-> DataFrame:
        """
        """
        table_df = self.current_table.data


        original_ignore_header = self.ignore_header

        # disable header for Parquet and overwrite ignore_header for validation keywords
        self.header = header if self.file_type != FileType.Parquet else False
        self.ignore_header = not self.header

        if self.header:
            headers = table_df.iloc[0].tolist()
            rows = table_df.iloc[1:]
            table_df = pd.DataFrame(rows.values, columns=headers)

        if column is not None and self.file_reader.validate_column(table_df, column):
            column = self.file_reader.cast_column_type(column)

        if row is not None:
            self.file_reader.validate_row(table_df, row)

        # Different actions
        if action == ModifyAction.Insert_Column:
            table_df = self.insert_column_to_dataframe(
                column,
                data,
                table_df
            )
        if action == ModifyAction.Insert_Row:
            table_df = self. insert_row_to_dataframe(
                row,
                data,
                table_df
            )
        if action == ModifyAction.Append_Column:
            table_df = self.append_column_to_dataframe(
                data,
                table_df
            )

        if action == ModifyAction.Append_Row:
            table_df = self.append_row_to_dataframe(
                data,
                table_df
            )
        if action == ModifyAction.Remove_Column:
            column_index = table_df.columns[column] if isinstance(column, int) else column
            table_df = table_df.drop(column_index, axis=1)

        if action == ModifyAction.Remove_Row:
            table_df = self.remove_row_dataframe(row, table_df)

        '''
        if header: # need to revert the table header after manipulation
            header = table_df.columns.to_list()
            data = table_df.values.tolist()
            combined_data = [header]
            combined_data.extend(data)
            table_df = DataFrame(combined_data)
        self.current_table.data = table_df'''

        self.ignore_header = original_ignore_header

        return table_df


