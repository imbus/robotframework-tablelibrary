from robot.api.deco import keyword
from ..general.library_attributes import LibraryAttributes
from ..utils.file_reader import FileReader
from ..utils import file_reader
from ..utils.settings import FileType
from typing import Any, cast
from pandas import DataFrame
from assertionengine import verify_assertion, AssertionOperator
from assertionengine.assertion_engine import NumericalOperators


class Getter(LibraryAttributes):

    def __init__(self, library):
        self.library = library
        self.file_reader = FileReader(library)


    @keyword(tags=["Getter"])
    def read_table(
            self,
            path: str
    ) -> list[list[Any]]:
        """
        """
        table_df = self.file_reader.read_table_file(path)
        data = cast(list[list[Any]], table_df.values.tolist())

        if self.file_type == FileType.Parquet and not self.ignore_header:
            data.insert(0, list(table_df.columns))

        return data


    @keyword(tags=["Getter"])
    def read_table_cell(
            self,
            data: list[list[Any]],
            row: int,
            column: int | str,
            assertion_operator: AssertionOperator | None = None,
            assertion_expected: Any = None,
            message: str = "",
        ) -> Any:
        """
        Keyword reads the table cell with the given row & column index.

        | =`Arguments`= | =`Description`= |
        | ``data`` | The table data - must be reat via ``Read`` keywords first |
        | ``row`` | Row to read the cell from |
        | ``column`` | Column to read the cell from |
        | ``assertion_operator`` | See ``robotframework-assertion-engine`` for more details.
        |                          Only numerical operators are allowed |
        | ``assertion_expected`` | See ``robotframework-assertion-engine`` for more details |
        | ``message`` | Custom error message for failed assertion |

        == Return Value / Errors ==
        Keyword returns the value of the given cell.\n
        In case of a failed assertion, the keyword will just fail without returning anything.

        == Example ==
        | CSV:
        | ${data} =    Read Table    ${CURDIR}/testdata/statistics.csv
        |
        | ${cell_value} =    Read Table Cell    ${data}    0    1    # without assertion
        | Read Table Cell    ${data}    0    1    ==    27    # with assertion
        |
        | Read Table Cell    ${data}    1    name    ==    sascha
        | # using column name 'name' and 1st index row and checking if its value is 'sascha'
        |
        """
        column = self.file_reader.cast_column_type(column)
        cell = None
        table_df = DataFrame(data)

        if self.file_reader.validate_column(table_df, column) and self.file_reader.validate_row(table_df, row):
            if isinstance(column, str):
                table_df = DataFrame(data[1:], columns=data[0])
                cell = table_df.loc[row, column]
            else:
                cell = table_df.iloc[row, column]

        if assertion_expected:
            if assertion_operator not in NumericalOperators:
                raise ValueError(f"Unexpected operator for assertion: {assertion_operator}. Use only {[op.value for op in NumericalOperators]}.")
            verify_assertion(
                cell,
                assertion_operator,
                assertion_expected,
                message
            )
        return cell

    @keyword(tags=["Getter"])
    def read_table_column(
            self,
            data: list[list[Any]],
            column: str | int,
            assertion_operator: AssertionOperator | None = None,
            assertion_expected: Any = None,
            message: str = "",
        ) -> list[Any]:
        """
        Keyword to read the given table column.

        | =`Arguments`= | =`Description`= |
        | ``data`` | The table data - must be reat via ``Read`` keywords first |
        | ``column`` | Column header name (str) or index (int) to return values from |
        | ``assertion_operator`` | See ``robotframework-assertion-engine`` for more details.
        |                          Only numerical operators are allowed |
        | ``assertion_expected`` | See ``robotframework-assertion-engine`` for more details |
        | ``message`` | Custom error message for failed assertion |

        == Example ==
        | CSV:
        | ${data} =    Read Table    ${CURDIR}/testdata/statistics.csv
        |
        | ${cell_value} =    Read Table Column    ${data}    0    # header index
        |
        | Tables.Configure Ignore Header    False
        | ${data} =    Tables.Read Table    example_01.csv
        | Read Table Column    ${data}    name    contains    alex
        | Read Table Column    ${data}    name    not contains    franz
        |
        | ${cell_value} =    Read Table Column    ${data}   Names    # header name
        """
        valid_assertions = [
            AssertionOperator["contains"],
            AssertionOperator["not contains"],
            AssertionOperator["validate"],
            ]
        column = self.file_reader.cast_column_type(column)
        column_list = []
        table_df = DataFrame(data)

        if self.file_reader.validate_column(table_df, column):
            if isinstance(column, str):
                table_df = DataFrame(data[1:], columns=data[0])
                column_list = table_df.loc[:,column]
            else:
                column_list = table_df.iloc[:,column]

            column_list = cast(list[Any], column_list.to_list())

        if assertion_expected:
            if assertion_operator not in valid_assertions:
                raise ValueError(f"Unexpected operator for assertion: {assertion_operator}. Use only {list(valid_assertions)}.")
            verify_assertion(
                column_list,
                assertion_operator,
                assertion_expected,
                message
            )

        return column_list

    @keyword(tags=["Getter"])
    def read_table_row(
            self,
            data: list[list[Any]],
            row: int,
            assertion_operator: AssertionOperator | None = None,
            assertion_expected: Any = None,
            message: str = "",
        ) -> list[Any]:
        """
        Keyword to read a specific row from the table data - row is specified by its index.

        | =`Arguments`= | =`Description`= |
        | ``data`` | The table data - must be reat via ``Read`` keywords first |
        | ``row`` | Row index (int) to read values from |
        | ``assertion_operator`` | See ``robotframework-assertion-engine`` for more details.
        |                          Only numerical operators are allowed |
        | ``assertion_expected`` | See ``robotframework-assertion-engine`` for more details |
        | ``message`` | Custom error message for failed assertion |

        == Example ==
        | CSV
        | Tables.Configure Ignore Header    True
        | ${data} =    Tables.Read Table    example_01.csv
        | Tables.Read Table Row 2    ${data}    0    contains    alex
        """
        valid_assertions = [
            AssertionOperator["contains"],
            AssertionOperator["not contains"],
            AssertionOperator["validate"],
            ]
        row_list = []
        table_df = DataFrame(data)

        if self.file_reader.validate_row(table_df, row):
            row_list = cast(list[Any], table_df.iloc[row].to_list())

        if assertion_expected:
            if assertion_operator not in valid_assertions:
                raise ValueError(f"Unexpected operator for assertion: {assertion_operator}. Use only {list(valid_assertions)}.")
            verify_assertion(
                row_list,
                assertion_operator,
                assertion_expected,
                message
            )

        return row_list

    @keyword(tags=["Getter"])
    def count_table(self,
                    axis: file_reader.Axis,
                    data: list[list[Any]],
                    assertion_operator: AssertionOperator | None = None,
                    assertion_expected: Any = None,
                    message: str = "",
                        ) -> int:
        """
        Keywod for counting rows or columns in the provided table.

        | =`Arguments`= | =`Description`= |
        | ``axis`` | Select 'Columns' or 'Rows' depending which axis should be checked |
        | ``data`` | The table data - must be reat via ``Read`` keywords first |
        | ``assertion_operator`` | See ``robotframework-assertion-engine`` for more details.
        |                          Only numerical operators are allowed |
        | ``assertion_expected`` | See ``robotframework-assertion-engine`` for more details |
        | ``message`` | Custom error message for failed assertion |

        == Example ==
        | CSV:
        | ${content} =    Tables.Read Table    example_01.csv
        | Tables.Count Table    Rows        ${content}    ==    ${6}
        | Tables.Count Table    Columns     ${content}    ==    ${3}
        """

        table_df = DataFrame(data)
        shape_index = 0 if axis == file_reader.Axis.Rows else 1

        axis_count = cast(int, table_df.shape[shape_index])

        if assertion_expected:
            if assertion_operator not in NumericalOperators:
                raise ValueError(f"Unexpected operator for assertion: {assertion_operator}. Use only {list(NumericalOperators)}.")
            verify_assertion(
                axis_count,
                assertion_operator,
                assertion_expected,
                message
            )

        return axis_count
