from robot.api.deco import keyword

from ..general.library_attributes import LibraryAttributes
from ..utils.file_reader import Axis
from ..utils.file_system import FileSystem
from ..utils.settings import FileType, TableFormat
from ..utils.file_access import FileAccess

from typing import Any, cast
from pathlib import Path
from typing import Literal
import pandas as pd

from assertionengine import verify_assertion, AssertionOperator
from assertionengine.assertion_engine import NumericalOperators



class Getter(LibraryAttributes):

    def __init__(self, library, file_access:FileAccess):
        self.library = library
        self.file_reader = file_access.file_reader

    @property
    def _fs(self):
        return FileSystem()

    @keyword(tags=["Getter"])
    def read_table(
            self,
            path: Path,
            return_type: Literal["Lists", "Dicts"] = "Lists"
    ) -> list[list] | list[dict[str, Any]]:
        """
        Keyword reads a table from the given path & returns the content.

        | =`Arguments`= | =`Description`= |
        | ``path`` | Specify the path of the given tables file. |

        == Return Value ==
        Keyword returns the complete content of the given file.\n
        Raises an error if the file does not exist!

        == Example ==
        | ${data} =    Read Table    ${CURDIR}/testdata/statistics.csv
        """
        table_df = self.file_reader.read_table_file(path)
        data = cast(list[list], table_df.values.tolist())

        if self.file_type == FileType.Parquet and not self.ignore_header:
            data.insert(0, list(table_df.columns))

        if self.ignore_header and self.file_type != FileType.Parquet:
                table_df = table_df.iloc[1:]
                data = data[1:]

        if return_type == "Dicts":
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
            alias: str,
            path: Path
    ) -> str:
        """"""
        self.file_reader.open_table_dataframe(
            alias= alias,
            path= path
        )
        return alias

    @keyword(tags=["Getter"])
    def close_table(
            self,
            alias: str | None = None
        ) -> bool:
        """"""
        expected: bool = self.file_reader.close_table_dataframe(alias=alias)
        return expected

    @keyword(tags=["Getter"])
    def switch_table(
            self,
            alias: str,
    ):
        """"""
        return self.file_reader.table_dataframe_switch(
            alias=alias
        )

    @keyword(tags=["Getter"])
    def get_table(
            self,
            return_type:TableFormat = TableFormat["List of lists"]
    ) -> list[list] | list[dict] | pd.DataFrame:
        """"""
        current_df = self.file_reader.file_sync.table_storage[self.file_reader.file_sync.current_file].data
        table_df = self.file_reader.validate_table_to_dataframe(
            data= current_df)

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
        | ${cell_value} =    Get Table Cell    ${data}    0    1    # without assertion
        | Get Table Cell    ${data}    0    1    ==    27    # with assertion
        |
        | Get Table Cell    ${data}    1    name    ==    sascha
        | # using column name 'name' and 1st index row and checking if its value is 'sascha'
        |
        """
        cell = None
        current_df = self.file_reader.file_sync.table_storage[self.file_reader.file_sync.current_file].data
        table_df = self.file_reader.validate_table_to_dataframe(
            data= current_df,
            row= row,
            column= column)


        column = self.file_reader.cast_column_type(column)

        cell = table_df.loc[row, column] if isinstance(column, str) else table_df.iloc[row, column]

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
    def get_table_column(
            self,
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
        | ${cell_value} =    Get Table Column    ${data}    0    # header index
        |
        | Tables.Configure Ignore Header    False
        | ${data} =    Tables.Read Table    example_01.csv
        | Get Table Column    ${data}    name    contains    alex
        | Get Table Column    ${data}    name    not contains    franz
        |
        | ${cell_value} =    Get Table Column    ${data}   Names    # header name
        """
        valid_assertions = [
            AssertionOperator["contains"],
            AssertionOperator["not contains"],
            AssertionOperator["validate"],
            ]
        column_list = []
        current_df = self.file_reader.file_sync.table_storage[self.file_reader.file_sync.current_file].data
        table_df = self.file_reader.validate_table_to_dataframe(
            data= current_df,
            column= column)
        column = self.file_reader.cast_column_type(column)

        column_df = table_df.loc[:,column] if isinstance(column, str) else table_df.iloc[:,column]
        column_list = cast(list[Any], column_df.to_list())

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
    def get_table_row(
            self,
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
        | Tables.Get Table Row 2    ${data}    0    contains    alex
        """
        valid_assertions = [
            AssertionOperator["contains"],
            AssertionOperator["not contains"],
            AssertionOperator["validate"],
            ]
        row_list = []
        current_df = self.file_reader.file_sync.table_storage[self.file_reader.file_sync.current_file].data
        table_df = self.file_reader.validate_table_to_dataframe(
            data= current_df,
            row= row)

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
                    path: Path | str,
                    axis: Axis,
                    assertion_operator: AssertionOperator | None = None,
                    assertion_expected: Any = None,
                    message: str = "",
                        ) -> int:
        """
        Keyword for counting rows or columns in the provided table.

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
        | Tables.Count Table    ${content}  Rows    ==    ${6}
        | Tables.Count Table    ${content}  Columns    ==    ${3}
        """
        casted_path = self.file_reader.cast_path_type(path)
        if isinstance(casted_path, Path):
            df = self.file_reader.read_table_file(casted_path)
        else:
            df = self.file_reader.file_sync.table_storage[casted_path].data

        table_df = self.file_reader.validate_table_to_dataframe(
            data= df)
        shape_index = 0 if axis == Axis.Rows else 1

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
