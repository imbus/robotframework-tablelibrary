from robot.api.deco import keyword
from ..general.library_attributes import LibraryAttributes
from ..utils.file_reader import FileReader
from ..utils.settings import FileType
from typing import Any
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
        ) -> Any:
        """
        Keyword to read the table data for the supported file types.
        """
        self.file_reader.file_exists(path)

        if self.file_type == FileType.CSV:
            return self.file_reader.read_csv(path)
        if self.file_type == FileType.Excel:
            dict_df = self.file_reader.read_excel(path)
            for sheet in dict_df:
                dict_df[sheet] = DataFrame(dict_df[sheet]).values.tolist()
            return dict_df
        if self.file_type == FileType.Parquet:
            return self.file_reader.read_parquet(path)
        raise ValueError(f"Not supported data type - file path: {path}")

    @keyword(tags=["Getter"])
    #v@config_validation
    def read_table_cell(
            self,
            data: list[list[Any]],
            row: int,
            column: int,
            assertion_operator: AssertionOperator | None = None,
            assertion_expected: Any = None,
            message: str = "",
        ):
        """
        Keyword reads the table cell with the given row & column index.
        """
        # if header is not ignored, we need to increase the row index
        if not self.ignore_header:
            row += 1

        try:
            cell = data[row][column]
        except IndexError as err:
            raise IndexError(
                f"Row / column index '{row} ; {column}' does not exist in your data object:\n{data}"
            ) from err
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

        == Arguments ==
        ``data`` : Pass the previously returned table data.
        ``column`` : Column header name as string value or column header index as integer value.
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
        return df[column].tolist()
