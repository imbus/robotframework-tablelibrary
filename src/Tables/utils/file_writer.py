from enum import Enum
from pathlib import Path
from typing import Any

import pandas as pd
from pandas import DataFrame

from ..general.library_attributes import LibraryAttributes
from ..utils.file_system import FileSync, FileSystem
from ..utils.settings import FileType, TableFormat
from .file_reader import FileReader


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

        self.header: bool = True

    @property
    def file_reader(self):
        return FileReader(self.library, FileSync)

    @property
    def _fs(self):
        return FileSystem()

    @property
    def _table_storage(self):
        return self.file_sync.table_storage

    @property
    def current_table(self):
        return self._table_storage[self.file_sync.current_file]

    def find_file_path(self, path: str | Path | None = None) -> Path:
        if path is None:
            return Path(self.current_table.path)
        casted_path = self.file_reader.cast_path_type(path)
        if isinstance(casted_path, str) and casted_path in self._table_storage:
            return Path(self._table_storage[casted_path].path)
            # raise ValueError(f"Couldn't find saved table. Current open tables are:"
            #                  f"{[self._table_storage.keys()]}")
        return Path(casted_path)

    def add_header_in_dataframe(self, table: DataFrame) -> DataFrame:
        """Adds header parameter to Dataframe if self.header = True. In case of Parquet:
        It already has pre-determined header so it will be extracted and put as data first. Then it will check self.header
        state and work as regular dataframe."""
        if self.file_type == FileType.Parquet:
            table_header = table.columns.to_list()
            table_data = table.values.tolist()
            header_data_table = [table_header]
            header_data_table.extend(table_data)
            table = DataFrame(header_data_table, columns=None)

        if self.header and not table.empty:
            headers = table.iloc[0].tolist()
            rows = table.iloc[1:]
            table = DataFrame(rows.values, columns=headers)
        return table

    def update_cached_dataframe(self, table: DataFrame) -> DataFrame:
        if self.file_sync.current_file is not None:
            table = self.file_reader.reset_header_dataframe(table)
            self.current_table.data = table
        return self.current_table.data

    def insert_column_to_dataframe(
        self,
        column_index: int | str | None,
        column_data: list | None,
        table: DataFrame,
    ) -> DataFrame:
        if column_index is None or column_data is None:
            raise ValueError(
                f"Cannot insert column if either column index ({column_index})or column data ({column_data}) is empty."
            )
        if isinstance(column_index, str):
            raise TypeError("Cannot modify table using column name as index. Use int instead")
        if self.file_type != FileType.Parquet:
            table = self.file_reader.reset_header_dataframe(
                table
            )  # we reset the headers since column index doesn't matter
        self.file_reader.validate_data_list_with_table(
            data=column_data, table=table, column=column_index
        )
        table.insert(
            loc=column_index, column=column_index, value=column_data, allow_duplicates=True
        )
        # reset column index in new dataframe
        return DataFrame(table.values)

    def insert_row_to_dataframe(
        self, row_index: int | None, row_data: list | None, table: DataFrame
    ) -> DataFrame:
        if row_index is None or row_data is None:
            raise ValueError(
                f"Cannot insert row if either row index ({row_index})or row data ({row_data}) is empty."
            )
        self.file_reader.validate_data_list_with_table(data=row_data, table=table, row=row_index)
        data_df = DataFrame(
            [row_data],
            columns=table.columns.to_list() if self.header else None,
        )

        return pd.concat(objs=[table[:row_index], data_df, table[row_index:]], ignore_index=True)

    def append_column_to_dataframe(
        self, column_data: list | str | None, table: DataFrame
    ) -> DataFrame:
        if column_data is None:
            raise ValueError(f"Cannot append column if column data({column_data}) is empty.")

        if self.file_type != FileType.Parquet:
            table = self.file_reader.reset_header_dataframe(
                table
            )  # we reset the headers since column index doesn't matter
        self.file_reader.validate_data_list_with_table(data=column_data, table=table, column=1)

        new_column_index = table.shape[1]
        table[new_column_index] = column_data

        return table

    def append_row_to_dataframe(self, row_data: list | None, table: DataFrame) -> DataFrame:
        if row_data is None:
            raise ValueError(f"Cannot append row if row data({row_data}) is empty.")

        # self.file_reader.validate_data_list_with_table(
        #         data=row_data,
        #         table=table,
        #         row=1
        #     )
        table.loc[len(table)] = row_data
        return table

    def remove_column_dataframe(
        self, column_index: str | int | None, table: DataFrame
    ) -> DataFrame:
        if column_index is None:
            raise ValueError(f"Cannot remove column if column index({column_index}) is empty.")

        column_index = (
            table.columns[column_index] if isinstance(column_index, int) else column_index
        )
        table = table.drop(column_index, axis=1)

        # reset the index since it got changed
        if not self.header:
            table.columns = range(table.shape[1])
        return table

    def remove_row_dataframe(self, row_index: int | None, table: DataFrame) -> DataFrame:
        if row_index is None:
            raise ValueError(f"Cannot remove row if row index({row_index}) is empty.")
        table = table.drop(row_index)
        return table.reset_index(drop=True)

    def write_table(
        self, data: DataFrame | list[list], file_path: Path | str | None = None
    ) -> Path:
        """Keyword to create/overwrite table using dataframe tables."""
        file_path = self.find_file_path(file_path)

        if isinstance(file_path, Path):
            dir_name = file_path.parent
            self._fs.ensure_directory_exists(dir_name)
        else:
            raise TypeError("Invalid file_path type.")

        self.file_type = self.file_reader.read_data_type(file_path)

        if isinstance(data, list) and self.file_type == FileType.Parquet:
            data_df = pd.DataFrame(data[1:], columns=data[0])
        elif isinstance(data, list) and self.file_type != FileType.Parquet:
            data_df = pd.DataFrame(data)
        else:
            data_df = data

        # lists or 'headless' dataframes automatically add index in to_csv. We prevent that by puting first row as header
        fixed_header = self.header and not isinstance(data, list)

        writers = {
            FileType.CSV: lambda: data_df.to_csv(
                file_path,
                index=False,
                header=fixed_header,
                sep=self.separator.value,
                quoting=self.quoting.value,
                quotechar=self.quoting_character.value,
            ),
            FileType.Excel: lambda: data_df.to_excel(file_path, index=False, header=fixed_header),
            FileType.Parquet: lambda: data_df.to_parquet(file_path),
        }

        writer = writers.get(self.file_type)
        if writer:
            writer()
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
        return file_path

    def set_dataframe_cells(
        self,
        data: Any,
        row: None | int = None,
        column: None | str | int = None,
        header: bool = True,
        return_type: TableFormat = TableFormat["Dataframe"],
    ) -> list[list] | list[dict] | DataFrame:
        """Changes a cell in a Dataframe."""
        table_df = self.current_table.data
        original_ignore_header = self.ignore_header
        original_header = self.header

        # overwrite ignore_header for validation keywords
        self.header = header
        self.ignore_header = not self.header

        table_df = self.add_header_in_dataframe(table_df)

        if isinstance(data, list):
            self.file_reader.validate_data_list_with_table(
                data=data,
                table=table_df,
                row=row,
                column=column,
            )

        axis_row = row if row is not None else slice(None)
        axis_column = (
            self.file_reader.cast_column_type(column) if column is not None else slice(None)
        )

        if column:
            self.file_reader.validate_column(table_df, axis_column)
        if row:
            self.file_reader.validate_row(table_df, axis_row)

        if isinstance(axis_column, str):
            table_df.loc[axis_row, axis_column] = data
        else:
            table_df.iloc[axis_row, axis_column] = data

        table_df = self.update_cached_dataframe(table_df)

        self.ignore_header = original_ignore_header
        self.header = original_header

        return self.file_reader.convert_dataframe(table_df, return_type)

    def modify_table(
        self,
        action: ModifyAction,
        data: list | None = None,
        row: int | None = None,
        column: str | int | None = None,
        header: bool = True,
    ) -> DataFrame:
        """
        Depending on the action this Keyword changes table data by removing,inserting or appending row or column.
        """
        table_df = self.current_table.data
        original_ignore_header = self.ignore_header
        original_header = self.header

        if action in {ModifyAction.Append_Column, ModifyAction.Insert_Column}:
            self.header = False
        else:
            self.header = header
        self.ignore_header = not self.header

        table_df = self.add_header_in_dataframe(table_df)

        if column is not None and self.file_reader.validate_column(table_df, column):
            column = self.file_reader.cast_column_type(column)

        if (
            row is not None
            and action is not ModifyAction.Append_Row
            and action is not ModifyAction.Append_Column
        ):
            self.file_reader.validate_row(table_df, row)

        # Different actions
        actions = {
            ModifyAction.Insert_Column: lambda: self.insert_column_to_dataframe(
                column, data, table_df
            ),
            ModifyAction.Insert_Row: lambda: self.insert_row_to_dataframe(row, data, table_df),
            ModifyAction.Append_Column: lambda: self.append_column_to_dataframe(data, table_df),
            ModifyAction.Append_Row: lambda: self.append_row_to_dataframe(data, table_df),
            ModifyAction.Remove_Column: lambda: self.remove_column_dataframe(column, table_df),
            ModifyAction.Remove_Row: lambda: self.remove_row_dataframe(row, table_df),
        }
        modify_action = actions.get(action)
        if modify_action:
            table_df = modify_action()
        else:
            raise ValueError(f"Invalid action. Available actions are: {list(ModifyAction)}")

        self.update_cached_dataframe(table_df)

        self.ignore_header = original_ignore_header
        self.header = original_header

        return table_df
