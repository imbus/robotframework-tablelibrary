from pathlib import Path
from typing import Any, cast
from uuid import uuid4

import pandas as pd
from assertionengine import AssertionOperator, verify_assertion
from assertionengine.assertion_engine import EvaluationOperators, NumericalOperators
from robot.api import logger
from robot.api.deco import keyword
from robot.api.exceptions import ContinuableFailure

from ..general.library_attributes import LibraryAttributes
from ..utils.file_access import FileAccess
from ..utils.file_reader import Axis
from ..utils.file_system import FileSystem
from ..utils.settings import FileType, TableFormat


class Getter(LibraryAttributes):
    def __init__(self, library, file_access: FileAccess):
        self.library = library
        self.file_reader = file_access.file_reader
        self.file_writer = file_access.file_writer

    @property
    def _fs(self):
        return FileSystem()

    @keyword(tags=["Getter"])
    def read_table(
        self, path: Path, return_type: TableFormat = TableFormat["List of lists"]
    ) -> list[list] | list[dict[str, Any]] | pd.DataFrame:
        """
        Keyword reads a table from the given path & returns the content.

        Args:
            path: Specify the path of the your table file.
            return_type: You can declare what type of table format it should be returned. Either list of lists, list of dictionaries or a pandas datarframe. Default: List of lists.

        Returns:
            Keyword returns the complete content of the given file.\n

        Raises:
            FileNotFoundError: Raises an error if the file does not exist!

        ## Example
        ```robotframework
        *** Test Cases ***
        Read Table
            ${data} =    Read Table    ${CURDIR}/testdata/statistics.csv    List of lists
            ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "index"
            BuiltIn.Should Be True    ${result} # checking if the first column is 'index'
        ```
        """
        table_df = self.file_reader.read_table_file(path)
        if return_type == TableFormat["Dataframe"]:
            return table_df
        data = cast(list[list], table_df.values.tolist())

        if self.file_type == FileType.Parquet and not self.ignore_header:
            data.insert(0, list(table_df.columns))

        if self.ignore_header and self.file_type != FileType.Parquet and len(data) > 1:
            table_df = table_df.iloc[1:]
            data = data[1:]

        data = self.file_reader.convert_missing_values(data)

        if return_type == TableFormat["List of dicts"]:
            df_for_dicts = table_df

            if self.file_type != FileType.Parquet and not self.ignore_header and not table_df.empty:
                header = [str(x) for x in df_for_dicts.iloc[0].tolist()]
                df_for_dicts = df_for_dicts.iloc[1:].copy()
                df_for_dicts.columns = header
            return self.file_reader.convert_missing_values(
                cast(list[dict[str, Any]], df_for_dicts.to_dict(orient="records"))
            )
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

        Args:
            path: Specify the path of the given table file.
            alias: Define an alias name to identify the opened table file.

        Returns:
            The alias string.

        ## Example
        ```robotframework
        *** Test Cases ***
        Open And Save Multiple Tables
            Tables.Open Table    table 1   table.csv
            Tables.Open Table    table 2   table_1.csv    # currently table 2 is active
        ```
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
        file_path: Path | None = None,
    ):
        """
        Keyword which creates a new internal empty table object which can be directly used to add data.
        Afterwards the data can be written into a new file.

        Creating a new empty table requires headers. This leads to a better understanding of the data for each column
        and wont be a problem for further workflows with the table data.

        Args:
            headers: Define headers for the new table file.
            alias: Optional. If not given, a UUID is generated as a unique alias.
            file_path: Optional. If given, the new table is immediately stored in the file system.

        ## Important
        Adding ``initial`` data to the empty table, MUST be done via ``Append Row`` or ``Append Column`` keyword - see example.

        ## Example
        This example creates a new empty table, appends row & columns and writes it to a new csv file.
        ```robotframework
        *** Test Cases ***
        Create And Write Table
            VAR    @{headers} =    name    age
            VAR    @{person_1} =    name    age
            ${uuid} =    Create Table    headers=${headers}
            Append Row    ${person_1}

            VAR    @{new_column} =    city    MG
            Append Column    ${new_column}

            Write Table    ${uuid}    ${filepath}
        ```
        """
        if not alias:
            alias = str(uuid4())

        fp = file_path if isinstance(file_path, Path) else "unknown"
        self.file_reader.create_empty_table_dataframe(alias, headers, fp)

        # if defined, create the initial file in your file system after creation
        if isinstance(file_path, Path):
            data = self.get_table(TableFormat.Dataframe)
            self.file_writer.write_table(data, file_path)

        return alias

    @keyword(tags=["Getter"])
    def close_table(self, alias: str | None = None) -> bool:
        """
        Keyword which closes specific or all of the tables.

        Args:
            alias: Use the alias of the saved table. If omitted, all opened tables are closed.

        Returns:
            ``True`` if the table is successfully closed; ``False`` if no tables are open.

        ## Example
        ```robotframework
        *** Test Cases ***
        Close A Table
            Tables.Open Table    table 1   table.csv
            Tables.Open Table    table 2   table_1.csv
            Tables.Close Table    table 1     # close table 1
        ```
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

        Args:
            alias: Use the alias of the saved table.

        Returns:
            The alias that was selected as the current table.

        ## Example
        ```robotframework
        *** Test Cases ***
        Switch Between Tables
            Tables.Open Table    table 1   table.csv
            Tables.Open Table    table 2   table_1.csv    # current active table
            Tables.Switch Table   table 1     # switch to table 1
        ```
        """
        self.file_reader.table_dataframe_switch(alias=alias)
        return alias

    @keyword(tags=["Getter"])
    def get_table(self, return_type: TableFormat = TableFormat["List of lists"]) -> list[list] | list[dict] | pd.DataFrame:
        """
        Keyword which returns a table in form of either list of lists, list of dicts, pandas dataframe.

        If ``Configure Missing As None`` is enabled, missing values are returned as Python ``None`` for list and dictionary results. DataFrame results are unchanged.

        Args:
            return_type: Choose the table format to return. Default: list of lists.

        Returns:
            The table as a list of lists, list of dictionaries, or DataFrame.

        ## Example
        ```robotframework
        *** Test Cases ***
        Get Table In Different Formats
            Tables.Open Table    table 1   table.csv
            @{lists} =        Tables.Get Table
            @{dicts} =        Tables.Get Table    List of dicts
            @{dataframe} =    Tables.Get Table    Dataframe
        ```
        """
        current_df = self.file_reader.file_sync.table_storage[self.file_reader.file_sync.current_file].data
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

        If ``Configure Missing As None`` is enabled, a missing cell is returned as
        Python ``None`` and assertions are evaluated against the converted value.

        Args:
            row: Row to read the cell from.
            column: Column to read from. Can be an index or a column name. A string requires ``ignore_header`` to be False.
            assertion_operator: See ``robotframework-assertion-engine`` for more details. Only numerical operators are allowed.
            assertion_expected: Expected value for the assertion.
            message: Custom error message for a failed assertion.

        Returns:
            The value of the selected cell.

        ## Example
        ```robotframework
        *** Test Cases ***
        Get A Table Cell
            Tables.Configure Ignore Header    False
            Tables.Open Table    table 1    ${CURDIR}${/}testdata${/}example_01.csv
            Get Table Cell    1    name    ==    sascha
        ```
        """
        cell = None
        current_df = self.file_reader.file_sync.table_storage[self.file_reader.file_sync.current_file].data
        table_df = self.file_reader.validate_table_to_dataframe(data=current_df, row=row, column=column)

        column = self.file_reader.cast_column_type(column)

        cell = table_df.loc[row, column] if isinstance(column, str) else table_df.iloc[row, column]
        cell = self.file_reader.convert_missing_values(cell)

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

        If ``Configure Missing As None`` is enabled, missing column values are returned
        as Python ``None`` and assertions are evaluated against the converted values.

        Args:
            column: Column header name or index to return values from.
            assertion_operator: See ``robotframework-assertion-engine`` for more details. Only collection operators are allowed.
            assertion_expected: Expected value for the assertion.
            message: Custom error message for a failed assertion.

        Returns:
            The selected column values as a list.

        ## Example
        ```robotframework
        *** Test Cases ***
        Get A Table Column
            Tables.Configure Ignore Header    False
            Tables.Open Table    table 1    example_01.csv
            Get Table Column    name    contains    alex
        ```
        """
        valid_assertions = [
            AssertionOperator["contains"],
            AssertionOperator["not contains"],
            AssertionOperator["validate"],
        ]
        column_list = []
        current_df = self.file_reader.file_sync.table_storage[self.file_reader.file_sync.current_file].data
        table_df = self.file_reader.validate_table_to_dataframe(data=current_df, column=column)
        column = self.file_reader.cast_column_type(column)

        column_df = table_df.loc[:, column] if isinstance(column, str) else table_df.iloc[:, column]
        column_list = self.file_reader.convert_missing_values(cast(list[Any], column_df.to_list()))

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

        If ``Configure Missing As None`` is enabled, missing row values are returned as
        Python ``None`` and assertions are evaluated against the converted values.

        Args:
            row: Row index to return values from.
            assertion_operator: See ``robotframework-assertion-engine`` for more details. Only collection operators are allowed.
            assertion_expected: Expected value for the assertion.
            message: Custom error message for a failed assertion.

        Returns:
            The selected row values as a list.

        ## Example
        ```robotframework
        *** Test Cases ***
        Get A Table Row
            Tables.Configure Ignore Header    False
            Tables.Open Table    table 1   example_01.csv
            Tables.Get Table Row    0    contains    age
        ```
        """
        valid_assertions = [
            AssertionOperator["contains"],
            AssertionOperator["not contains"],
            AssertionOperator["validate"],
        ]
        row_list = []
        current_df = self.file_reader.file_sync.table_storage[self.file_reader.file_sync.current_file].data
        table_df = self.file_reader.validate_table_to_dataframe(data=current_df, row=row)

        row_list = self.file_reader.convert_missing_values(cast(list[Any], table_df.iloc[row].to_list()))

        if assertion_expected:
            if assertion_operator not in valid_assertions:
                raise ValueError(
                    f"Unexpected operator for assertion: {assertion_operator}. Use only {list(valid_assertions)}."
                )
            verify_assertion(row_list, assertion_operator, assertion_expected, message)

        return row_list

    @keyword(tags=["Getter"])
    def count_table(  # noqa PLR0913
        self,
        path: Path | str,
        axis: Axis,
        assertion_operator: AssertionOperator | None = None,
        assertion_expected: Any = None,
        message: str = "",
        continue_on_failure: bool = True,
    ) -> int:
        """
        Keyword for counting rows or columns in the provided table.

        Args:
            path: File path or alias returned by ``Open Table``.
            axis: Select ``Columns`` or ``Rows`` to determine what is counted.
            assertion_operator: See ``robotframework-assertion-engine`` for more details. Numerical and evaluation operators are allowed.
            assertion_expected: Expected count for the assertion.
            message: Custom error message for a failed assertion.
            continue_on_failure: Whether the test should continue after a failed assertion.

        Returns:
            The number of rows or columns.

        ## Example
        ```robotframework
        *** Test Cases ***
        Count Table Rows And Columns
            # CSV
            VAR    ${file_path}      ${CURDIR}${/}testdata${/}example_01.csv
            Tables.Open Table     table 1    ${file_path}
            Tables.Count Table    table 1    Rows       ==    ${6}
            Tables.Count Table    table 1    Columns    ==    ${3}

            VAR    ${file_path}      ${CURDIR}${/}testdata${/}example_01.csv
            ${row_count}  Tables.Count Table    ${file_path}    Rows
            BuiltIn.Should Be Equal    ${row_count}    ${6}
        ```
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

        # debugging
        logger.debug(f"Count of {axis.name}: {axis_count}")

        if assertion_expected:
            if assertion_operator in NumericalOperators or assertion_operator in EvaluationOperators:
                try:
                    verify_assertion(axis_count, assertion_operator, assertion_expected, message)
                except AssertionError as e:
                    err = message if message else str(e)
                    if not continue_on_failure:
                        raise AssertionError(err)  # noqa: B904
                    raise ContinuableFailure(err)  # noqa: B904
                except Exception:
                    raise
            else:
                raise ValueError(
                    f"Unexpected operator for assertion: {assertion_operator}. Use only {list(NumericalOperators)} or {list(EvaluationOperators)}."
                )
        return axis_count
