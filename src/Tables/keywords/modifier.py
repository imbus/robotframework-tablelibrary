from pandas import DataFrame
from robot.api.deco import keyword

from ..general.library_attributes import LibraryAttributes
from ..utils.file_access import FileAccess
from ..utils.file_writer import ModifyAction


class Modifier(LibraryAttributes):
    def __init__(self, library, file_access: FileAccess):
        self.library = library
        self.file_writer = file_access.file_writer

    @keyword(tags=["Writer"])
    def insert_row(self, row_data: list, row_index: int, header: bool = True) -> DataFrame:
        """
        Keyword to insert a new row into the currently opened table (see 'Open Table') at the given index.

        | =`Arguments`= | =`Description`= |
        | ``row_data`` | List of values which should be inserted to the table. Must match the lenght of table row.  |
        | ``row_index`` | Define the index of the row to modify. |
        | ``header`` | Set to ``True`` if header should be recognized during file modifications - if ``False`, its ignored. If Header = False and row index = 0 it will overwrite a possible header, if there is one! |

        == Return Value ==
        Returns the dataframe of the changed table.

        == Example ==
        | VAR    ${csv_path} =   test_writer.csv
        | VAR    @{row_list} =     2001    04
        | VAR    @{column_list} =   column 1    column 2

        | Tables.Open Table    table 1    ${csv_path}
        | Tables.Insert Row    ${row_list}    0    header=True      # inserting the 0 row with a header in mind
        | Tables.Insert Row    ${column_list}    0    header=False  # inserting the 0 row with no header in mind
        """

        return self.file_writer.modify_table(
            action=ModifyAction.Insert_Row, data=row_data, row=row_index, header=header
        )

    @keyword(tags=["Writer"])
    def insert_column(self, column_data: list, column_index: int) -> DataFrame:
        """
        Keyword to insert a new column into the currently opened table (see 'Open Table') at the given index.

        | =`Arguments`= | =`Description`= |
        | ``column_data`` | List of values which should be inserted to the table. Must match the size of table column. |
        | ``column_index`` | Define the index of the column to modify. |

        == Return Value ==
        Returns the dataframe of the changed table.

        == Example ==
        | VAR    ${csv_path} =   test_writer.csv
        | VAR    @{column_list} =    month      june      july

        | Tables.Open Table    table 1    ${csv_path}
        | Tables.Insert Column    ${column_list}        1   # inserting between index 0 and 1
        """

        return self.file_writer.modify_table(
            action=ModifyAction.Insert_Column,
            data=column_data,
            column=column_index,
        )

    @keyword(tags=["Writer"])
    def append_row(self, row_data: list) -> DataFrame:
        """
        Keyword to append a new row into the currently opened table (see 'Open Table') at the end of the table.

        | =`Arguments`= | =`Description`= |
        | ``row_data`` | List of values which should be inserted to the table. Must match the lenght of table row. |

        == Return Value ==
        Returns the dataframe of the changed table.

        == Example ==
        | VAR    ${csv_path} =   test_writer.csv
        | VAR    @{row_list} =     2001    04

        | Tables.Open Table    table 1    ${csv_path}
        | Tables.Append Row    ${row_list}
        """

        return self.file_writer.modify_table(action=ModifyAction.Append_Row, data=row_data, row=1)

    @keyword(tags=["Writer"])
    def append_column(
        self,
        column_data: list,
    ) -> DataFrame:
        """
        Keyword to append a new column into the currently opened table (see 'Open Table') at the end of the table.

        | =`Arguments`= | =`Description`= |
        | ``column_data`` | List of values which should be inserted to the table. Must match the lenght of table column. |

        == Return Value ==
        Returns the dataframe of the changed table.

        == Example ==
        | VAR    ${csv_path} =   test_writer.csv
        | VAR    @{column_list} =    month      june      july


        | Tables.Open Table    table 1    ${csv_path}
        | Tables.Append Column    ${column_list}
        """

        return self.file_writer.modify_table(
            action=ModifyAction.Append_Column,
            data=column_data,
            column=1,
        )

    @keyword(tags=["Writer"])
    def remove_row(self, row_index: int, header: bool = True) -> DataFrame:
        """
        Keyword to remove the given row from the currently opened table (see 'Open Table').

        | =`Arguments`= | =`Description`= |
        | ``row_index`` | Define the index of the row to modify. |
        | ``header`` | Set to ``True`` if header should be recognized during file modifications - if ``False`, its ignored. If Header = False and row index = 0 it will remove a possible header, if there is one!|

        == Return Value ==
        Returns the dataframe of the changed table.

        == Example ==
        | VAR    ${csv_path} =   test_writer.csv


        | Tables.Open Table    table 1    ${csv_path}
        | Tables.Remove Row    1    header=True     # remove the 1st row after the header
        | Tables.Remove Row    0    header=False     # remove the 0st row without headers
        """

        return self.file_writer.modify_table(
            action=ModifyAction.Remove_Row, row=row_index, header=header
        )

    @keyword(tags=["Writer"])
    def remove_column(
        self,
        column_index: int | str,
    ) -> DataFrame:
        """
        Keyword to remove the given column from the currently opened table (see 'Open Table').

        | =`Arguments`= | =`Description`= |
        | ``column_index`` | Define the index of the column to remove. It can be either an integer (index) or a string.|

        == Return Value ==
        Returns the dataframe of the changed table.

        == Example ==
        | VAR    ${csv_path} =   test_writer.csv


        | Tables.Open Table    table 1    ${csv_path}
        | Tables.Remove Column    0         # remove the very first column
        | Tables.Remove Column    temp      # remove the column with a header (or first row) called 'temp'
        """

        return self.file_writer.modify_table(
            action=ModifyAction.Remove_Column,
            column=column_index,
        )
