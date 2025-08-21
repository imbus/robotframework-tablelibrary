from robot.api.deco import keyword
from ..general.library_attributes import LibraryAttributes
from ..utils.file_reader import FileReader
from ..utils.settings import FileType
from typing import Any, cast
from pandas import DataFrame
from assertionengine import verify_assertion, AssertionOperator


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
        | ``assertion_operator`` | See ``robotframework-assertion-engine`` for more details |
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
        table_df = DataFrame(data)
        column = self.file_reader.cast_column_type(column)
        cell = None

        if self.file_reader.validate_column(table_df, column) and self.file_reader.validate_row(table_df, row):
            if isinstance(column, str):
                table_df = DataFrame(data[1:], columns=data[0])
                cell = table_df.loc[row, column]
            else:
                cell = table_df.iloc[row, column]

        if assertion_expected:
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
            column: str | int
        ) -> list[Any]:
        """
        Keyword to read the given table column.

        | =`Arguments`= | =`Description`= |
        | ``data`` | The table data - must be reat via ``Read`` keywords first |
        | ``column`` | Column header name (str) or index (int) to return values from |

        == Example ==
        | CSV:
        | ${data} =    Read Table    ${CURDIR}/testdata/statistics.csv
        |
        | ${cell_value} =    Read Table Column    ${data}    0    # header index
        |
        |
        | Excel:
        | Excel Open    excel_01    ${CURDIR}/testdata/example_06.xlsx
        |
        | ${data} =    Excel Sheet Read    Personen
        |
        | ${cell_value} =    Read Table Column    ${data}   Names    # header name
        """
        if self.ignore_header and isinstance(column, str):
            raise TypeError(
                "Column identifier cannot be 'str' type, when library setting 'ignore_header' is 'True'!"
            )

        # Convert to DataFrame with / without column headers

        df = DataFrame(data[1:], columns=data[0]) if not self.ignore_header else DataFrame(data)

        # Read column via str or int identifier
        if isinstance(column, int):
            column = df.columns[column]
        return cast(list[Any], df[column].tolist())



    @keyword(tags=["Getter"])
    def read_table_row(
            self,
            data: list[list[Any]],
            row: int
        ) -> list[Any]:
        """
        Keyword to read a specific row from the table data - row is specified by its index.

        | =`Arguments`= | =`Description`= |
        | ``data`` | The table data - must be reat via ``Read`` keywords first |
        | ``row`` | Row index (int) to read values from |

        == Example ==
        """
        if len(data) == 0:
            raise ValueError(
                f"Data object ccontains no data! Length of given list: {len(data)}"
            )
        df = DataFrame(data[1:], columns=data[0]) if not self.ignore_header else DataFrame(data)
        if row < 0 or row >= len(df):
            raise IndexError(f"Row index {row} out of range (0-{len(df)-1})")
        return cast(list[Any], df.iloc[row].tolist())
