from robot.api.deco import keyword
from ..general.library_attributes import LibraryAttributes
from ..utils.file_writer import ModifyAction
from ..utils.file_access import FileAccess

from pandas import DataFrame

class Modifier(LibraryAttributes):

    def __init__(self, library, file_access:FileAccess):
        self.library = library
        self.file_writer = file_access.file_writer

    @keyword(tags=['Writer'])
    def insert_row(
            self,
            row_data: list,
            row_index: int,
            header: bool = True
        ) -> DataFrame:
        """
        Keyword to insert a new row into the given data at the given index.
        """

        return self.file_writer.modify_table(
            action=ModifyAction.Insert_Row,
            data=row_data,
            row=row_index,
            header=header
        )

    @keyword(tags=['Writer'])
    def insert_column(
            self,
            column_data: list,
            column_index: int,
            header: bool = True
        )-> DataFrame:
        """
        Keyword to insert a new column into the given data at the given index.
        """

        return self.file_writer.modify_table(
                action=ModifyAction.Insert_Column,
                data=column_data,
                column=column_index,
                header=header
            )

    @keyword(tags=['Writer'])
    def append_row(
            self,
            row_data: list,
            header: bool = True
        ) -> DataFrame:
        """
        Keyword to append a new row at the end of the given data.
        """

        return self.file_writer.modify_table(
                action=ModifyAction.Append_Row,
                data=row_data,
                row=1,
                header=header
            )

    @keyword(tags=['Writer'])
    def append_column(
            self,
            column_data: list,
            header: bool = True
        ) -> DataFrame:
        """
        Keyword to append a new column at the end of the given data.
        """

        return self.file_writer.modify_table(
                action=ModifyAction.Append_Column,
                data=column_data,
                column=1,
                header=header
            )

    @keyword(tags=['Writer'])
    def remove_row(
            self,
            row_index: int,
            header: bool = True
        ) -> DataFrame:
        """
        Keyword to remove the given row from the given data.
        """

        return self.file_writer.modify_table(
            action=ModifyAction.Remove_Row,
            row=row_index,
            header=header
            )

    @keyword(tags=['Writer'])
    def remove_column(
            self,
            column_index: int | str,
            header: bool = True
        ) -> DataFrame:
        """
        Keyword to remove the given column from the given data.
        """

        return self.file_writer.modify_table(
                action=ModifyAction.Remove_Column,
                column=column_index,
                header=header
                )
