from robot.api.deco import keyword
from ..general.library_attributes import LibraryAttributes

class Modifier(LibraryAttributes):

    def __init__(self, library):
        self.library = library

    @keyword(tags=['Writer'])
    def insert_row(
            self,
            data: str,
            row: int,
            row_data
        ):
        """
        Keyword to insert a new row into the given data at the given index.
        """
        print("To be implemented")

    @keyword(tags=['Writer'])
    def insert_column(
            self,
            data: str,
            column: int,
            column_data
        ):
        """
        Keyword to insert a new column into the given data at the given index.
        """
        print("To be implemented")

    @keyword(tags=['Writer'])
    def append_row(
            self,
            data: str,
            row_data
        ):
        """
        Keyword to append a new row at the end of the given data.
        """
        print("To be implemented")

    @keyword(tags=['Writer'])
    def append_column(
            self,
            data: str,
            column_data
        ):
        """
        Keyword to append a new column at the end of the given data.
        """
        print("To be implemented")

    @keyword(tags=['Writer'])
    def remove_row(
            self,
            data: str,
            row: int
        ):
        """
        Keyword to remove the given row from the given data.
        """
        print("To be implemented")

    @keyword(tags=['Writer'])
    def remove_column(
            self,
            data: str,
            column: int | str
        ):
        """
        Keyword to remove the given column from the given data.
        """
        print("To be implemented")
