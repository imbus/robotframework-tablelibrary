from pathlib import Path
from typing import Any, cast
from uuid import uuid4

import pandas as pd
from assertionengine import AssertionOperator, verify_assertion
from assertionengine.assertion_engine import EvaluationOperators, NumericalOperators
from robot.api.deco import keyword

from ..general.library_attributes import LibraryAttributes
from ..utils.file_access import FileAccess
from ..utils.file_reader import Axis
from ..utils.file_system import FileSystem
from ..utils.settings import FileType, TableFormat


class Getter(LibraryAttributes):
    def __init__(self, library, file_access: FileAccess):
        self.library = library
        self.file_reader = file_access.file_reader

    @property
    def _fs(self):
        return FileSystem()

    @keyword(tags=["Getter"])
    def read_table(
        self, path: Path, return_type: TableFormat = TableFormat["List of lists"]
    ) -> list[list] | list[dict[str, Any]] | pd.DataFrame:
        """
        Keyword reads a table from the given path & returns the content.

        | =`Arguments`= | =`Description`= |
        | ``path`` | Specify the path of the your table file. |
        | ``return_type`` | You can declare what type of table format it should be returned. Either list of lists, list of dictionaries or a pandas datarframe. Default: List of lists. |

        == Return Value ==
        Keyword returns the complete content of the given file.\n
        Raises an error if the file does not exist!

        == Example ==
        | ${data} =    Read Table    ${CURDIR}/testdata/statistics.csv    List of lists
        | ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "index"
        | BuiltIn.Should Be True    ${result} # checking if the first column is 'index'
        """
        table_df = self.file_reader.read_table_file(path)
        if return_type == TableFormat["Dataframe"]:
            return table_df
        data = cast(list[list], table_df.values.tolist())

        if self.file_type == FileType.Parquet and not self.ignore_header:
            data.insert(0, list(table_df.columns))

        if self.ignore_header and self.file_type != FileType.Parquet:
            table_df = table_df.iloc[1:]
            data = data[1:]

        if return_type == TableFormat["List of dicts"]:
            df_for_dicts = table_df

            if self.file_type != FileType.Parquet and not self.ignore_header and not table_df.empty:
                header = [str(x) for x in df_for_dicts.iloc[0].tolist()]
                df_for_dicts = df_for_dicts.iloc[1:].copy()
                df_for_dicts.columns = header
            return cast(list[dict[str, Any]], df_for_dicts.to_dict(orient="records"))
        return data

    @keyword(tags=["Getter"])
    def open_table(
        self,
        path: Path,
        alias: str | None = None,
    ) -> str:
        """
        Keyword which is similar to read_table but saves the table in form of an alias.
        The saved table can be further modified but it will not change the file which was the table was opened from.

        | =`Arguments`= | =`Description`= |
        | ``path`` | Specify the path of the given tables file. |
        | ``alias`` | Define an alias name to identified opened table file. |

        == Return Value ==
        Returns the alias string.

        == Example ==
        | # Opening and saving multiple tables in cache
        | Tables.Open Table    table 1   table.csv
        | Tables.Open Table    table 2   table_1.csv    # currently table 2 is active
        """
        if not alias:
            alias = str(uuid4())

        self.file_reader.open_table_dataframe(alias=alias, path=path)
        return alias

    @keyword(tags=["Getter"])
    def create_table(
        self,
        headers: list,
        alias: str | None = None,
    ):
        """
        Keyword which creates a new internal empty table object which can be directly used to add data.
        Afterwards the data can be written into a new file.

        Creating a new empty table requires headers. This leads to a better understanding of the data for each column
        and wont be a problem for further workflows with the table data.

        == Arguments ==
        | =Argument= | =Description= |
        | ``headers`` | Define headers for the new table file. |
        | ``alias`` | Optional - if not given, uuid is generated as unique alias. |

        == Important ==

        Adding ``initial`` data to the empty table, MUST be done via ``Append Row`` or ``Append Column`` keyword - see example.

        == Example ==
        This example creates a new empty table, appends row & columns and writes it to a new csv file.
        |  VAR    @{headers} =    name    age
        |  VAR    @{person_1} =    name    age
        |  ${uuid} =    Create Table    headers=${headers}
        |  Append Row    ${person_1}
        |
        |  VAR    @{new_column} =    city    MG
        |  Append Column    ${new_column}
        |
        |  Write Table    ${uuid}    ${filepath}
        """
        if not alias:
            alias = str(uuid4())

        self.file_reader.create_empty_table_dataframe(alias, headers)
        return alias

    @keyword(tags=["Getter"])
    def close_table(self, alias: str | None = None) -> bool:
        """
        Keyword which closes specific or all of the tables.

        | =`Arguments`= | =`Description`= |
        | ``alias`` | Use the name of saved alias. If None was selected, then all copened tables will be closed. |

        == Return Value ==
        Returns True if the table is successfully closed. False if no open tables are available.

        == Example ==
        | Tables.Open Table    table 1   table.csv
        | Tables.Open Table    table 2   table_1.csv
        |
        | Tables.Close Table    table 1     # close table 1
        """
        expected: bool = self.file_reader.close_table_dataframe(alias=alias)
        return expected

    @keyword(tags=["Getter"])
    def switch_table(
        self,
        alias: str,
    ) -> str:
        """
        Keyword which switches into current working table.

        | =`Arguments`= | =`Description`= |
        | ``alias`` | Use the name of saved alias. |

        == Return Value ==
        Return the string of the alias it switched to.

        == Example ==
        | Tables.Open Table    table 1   table.csv
        | Tables.Open Table    table 2   table_1.csv    # current active table
        |
        | Tables.Switch Table   table 1     # switched to 'table 1' as current active table
        """
        self.file_reader.table_dataframe_switch(alias=alias)
        return alias

    @keyword(tags=["Getter"])
    def get_table(
        self, return_type: TableFormat = TableFormat["List of lists"]
    ) -> list[list] | list[dict] | pd.DataFrame:
        """
        Keyword which returns a table in form of either list of lists, list of dicts, pandas dataframe.

        | =`Arguments`= | =`Description`= |
        | ``return_type`` | Choose what type of table format it should return. Default: list of lists|

        == Return Value ==
        Return table in form as either list of lists, list of dicts or dataframe.

        == Example ==
        | Tables.Open Table    table 1   table.csv
        | @{lists} =        Tables.Get Table
        | @{dicts} =        Tables.Get Table    List of dicts
        | @{dataframe} =    Tables.Get Table    Dataframe
        """
        current_df = self.file_reader.file_sync.table_storage[
            self.file_reader.file_sync.current_file
        ].data
        table_df = self.file_reader.validate_table_to_dataframe(data=current_df)

        return self.file_reader.convert_dataframe(table_df, return_type)

    @keyword(tags=["Getter"])
    def get_table_cell(
        self,
        row: int,
        column: int | str,
        assertion_operator: AssertionOperator | None = None,
        assertion_expected: Any = None,
        message: str = "",
    ) -> Any:
        """
        Keyword reads the currently opened table cell (see opened_table) with the given row & column index.

        | =`Arguments`= | =`Description`= |
        | ``row`` | Row to read the cell from |
        | ``column`` | Column to read the cell from. Can be index number or a name of a column as a string. If string, ignore_header must be False. |
        | ``assertion_operator`` | See ``robotframework-assertion-engine`` for more details.  Only numerical operators are allowed |
        | ``assertion_expected`` | See ``robotframework-assertion-engine`` for more details |
        | ``message`` | Custom error message for failed assertion |

        == Return Value ==
        Keyword returns the value of the given cell.
        In case of a failed assertion, the keyword will just fail without returning anything.

        == Example ==
        | Tables.Configure Ignore Header    False
        | Tables.Open Table    table 1    ${CURDIR}${/}testdata${/}example_01.csv
        | Get Table Cell    1    name    ==    sascha
        """
        cell = None
        current_df = self.file_reader.file_sync.table_storage[
            self.file_reader.file_sync.current_file
        ].data
        table_df = self.file_reader.validate_table_to_dataframe(
            data=current_df, row=row, column=column
        )

        column = self.file_reader.cast_column_type(column)

        cell = table_df.loc[row, column] if isinstance(column, str) else table_df.iloc[row, column]

        if assertion_expected:
            if assertion_operator not in NumericalOperators:
                raise ValueError(
                    f"Unexpected operator for assertion: {assertion_operator}. Use only {[op.value for op in NumericalOperators]}."
                )
            verify_assertion(cell, assertion_operator, assertion_expected, message)
        return cell

    @keyword(tags=["Getter"])
    def get_table_column(
        self,
        column: str | int,
        assertion_operator: AssertionOperator | None = None,
        assertion_expected: Any = None,
        message: str = "",
    ) -> list[Any]:
        """
        Keyword to read the given table column from current opened table (see open_table).
        If ignore_header = True and searched column is a string then it will raise an error.

        | =`Arguments`= | =`Description`= |
        | ``column`` | Column header name (str) or index (int) to return values from |
        | ``assertion_operator`` | See ``robotframework-assertion-engine`` for more details. Only numerical operators are allowed |
        | ``assertion_expected`` | See ``robotframework-assertion-engine`` for more details |
        | ``message`` | Custom error message for failed assertion |

        == Return Value ==
        Returns column values as a list.

        == Example ==
        | Tables.Configure Ignore Header    False
        | Tables.Open Table    table 1    example_01.csv
        | Get Table Column    name    contains    alex
        """
        valid_assertions = [
            AssertionOperator["contains"],
            AssertionOperator["not contains"],
            AssertionOperator["validate"],
        ]
        column_list = []
        current_df = self.file_reader.file_sync.table_storage[
            self.file_reader.file_sync.current_file
        ].data
        table_df = self.file_reader.validate_table_to_dataframe(data=current_df, column=column)
        column = self.file_reader.cast_column_type(column)

        column_df = table_df.loc[:, column] if isinstance(column, str) else table_df.iloc[:, column]
        column_list = cast(list[Any], column_df.to_list())

        if assertion_expected:
            if assertion_operator not in valid_assertions:
                raise ValueError(
                    f"Unexpected operator for assertion: {assertion_operator}. Use only {list(valid_assertions)}."
                )
            verify_assertion(column_list, assertion_operator, assertion_expected, message)

        return column_list

    @keyword(tags=["Getter"])
    def get_table_row(
        self,
        row: int,
        assertion_operator: AssertionOperator | None = None,
        assertion_expected: Any = None,
        message: str = "",
    ) -> list[Any]:
        """
        Keyword to read the given table column from current opened table (see open_table).
        | =`Arguments`= | =`Description`= |
        | ``row`` | Row index (int) to read values from |
        | ``assertion_operator`` | See ``robotframework-assertion-engine`` for more details. Only numerical operators are allowed. |
        | ``assertion_expected`` | See ``robotframework-assertion-engine`` for more details |
        | ``message`` | Custom error message for failed assertion |

        == Return Value ==
        Returns row values as a list.

        == Example ==
        | Tables.Configure Ignore Header    False
        | Tables.Open Table    table 1   example_01.csv
        | Tables.Get Table Row    0    contains    age
        """
        valid_assertions = [
            AssertionOperator["contains"],
            AssertionOperator["not contains"],
            AssertionOperator["validate"],
        ]
        row_list = []
        current_df = self.file_reader.file_sync.table_storage[
            self.file_reader.file_sync.current_file
        ].data
        table_df = self.file_reader.validate_table_to_dataframe(data=current_df, row=row)

        row_list = cast(list[Any], table_df.iloc[row].to_list())

        if assertion_expected:
            if assertion_operator not in valid_assertions:
                raise ValueError(
                    f"Unexpected operator for assertion: {assertion_operator}. Use only {list(valid_assertions)}."
                )
            verify_assertion(row_list, assertion_operator, assertion_expected, message)

        return row_list

    @keyword(tags=["Getter"])
    def count_table(
        self,
        path: Path | str,
        axis: Axis,
        assertion_operator: AssertionOperator | None = None,
        assertion_expected: Any = None,
        message: str = "",
    ) -> int:
        """
        Keyword for counting rows or columns in the provided table.

        | =`Arguments`= | =`Description`= |
        | ``path`` | Either a filepath or a saved variable of 'Open Table' keyword. |
        | ``axis`` | Select 'Columns' or 'Rows' depending which axis should be checked |
        | ``assertion_operator`` | See ``robotframework-assertion-engine`` for more details. Only numerical operators are allowed |
        | ``assertion_expected`` | See ``robotframework-assertion-engine`` for more details |
        | ``message`` | Custom error message for failed assertion |

        == Return Value ==
        Keyword returns a number count of either rows or columns.

        == Example ==
        | CSV:
        | VAR    ${file_path}      ${CURDIR}${/}testdata${/}example_01.csv
        | Tables.Open Table     table 1    ${file_path}
        | Tables.Count Table    table 1    Rows     ==    ${6}
        | Tables.Count Table    table 1    Columns    ==    ${3}
        |
        | VAR    ${file_path}      ${CURDIR}${/}testdata${/}example_01.csv
        | ${row_count}  Tables.Count Table    ${file_path}    Rows
        | BuiltIn.Should Be Equal    ${row_count}    ${6}
        """
        casted_path = self.file_reader.cast_path_type(path)
        if isinstance(casted_path, Path):
            df = self.file_reader.read_table_file(casted_path)
        else:
            df = self.file_reader.file_sync.table_storage[casted_path].data

        if self.file_type == FileType.Parquet and not self.ignore_header:
            table_header = df.columns.to_list()
            table_data = df.values.tolist()
            header_data_table = [table_header]
            header_data_table.extend(table_data)
            df = pd.DataFrame(header_data_table, columns=None)

        table_df = self.file_reader.validate_table_to_dataframe(data=df)
        shape_index = 0 if axis == Axis.Rows else 1

        axis_count = cast(int, table_df.shape[shape_index])

        if assertion_expected:
            if (
                assertion_operator in NumericalOperators
                or
                assertion_operator in EvaluationOperators
            ):
                verify_assertion(axis_count, assertion_operator, assertion_expected, message)
            else:
                raise ValueError(
                    f"Unexpected operator for assertion: {assertion_operator}. Use only {list(NumericalOperators)}."
                )
        return axis_count
