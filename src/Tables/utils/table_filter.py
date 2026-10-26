from decimal import Decimal, InvalidOperation
from typing import Any, cast

import pandas as pd
from assertionengine import AssertionOperator, verify_assertion

from .file_reader import FileReader
from .settings import FileType, TableFormat


class TableFilter:
    def __init__(self, file_reader: FileReader):
        """Create a filtering service using the library's active FileReader state."""
        self.file_reader = file_reader

    def _prepare_table(
        self,
        current_df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, bool]:
        """Normalize header rows into columns and report whether output must restore the header row."""
        table_df = current_df.copy()
        has_header_row = False
        if self.file_reader.file_type == FileType.Parquet or not self.file_reader.check_default_dataframe_header(table_df):
            return table_df, has_header_row
        if self.file_reader.ignore_header:
            return self.file_reader.validate_table_to_dataframe(data=table_df), has_header_row
        if table_df.empty:
            return table_df, has_header_row

        header = table_df.iloc[0].tolist()
        table_df = table_df.iloc[1:].copy().reset_index(drop=True)
        table_df.columns = header
        return table_df, True

    @staticmethod
    def _to_decimal(value: Any) -> Decimal | None:
        """Convert a finite, non-boolean numeric value to Decimal; return None if it is not numeric."""
        if isinstance(value, bool):
            return None
        try:
            converted = Decimal(str(value))
        except (InvalidOperation, ValueError):
            return None
        return converted if converted.is_finite() else None

    @staticmethod
    def _is_missing(value: Any) -> bool:
        """Return whether a scalar is None or a pandas-recognized missing value."""
        if value is None:
            return True
        try:
            return bool(pd.isna(value))
        except (TypeError, ValueError):
            return False

    def _coerce_operands(
        self,
        value: Any,
        assertion_operator: AssertionOperator,
        assertion_expected: Any,
    ) -> tuple[Any, Any] | None:
        """Normalize numeric operands without changing textual comparisons or losing integer precision."""
        numeric_order_operators = {
            AssertionOperator["<"],
            AssertionOperator["<="],
            AssertionOperator[">"],
            AssertionOperator[">="],
        }
        numeric_equality = assertion_operator in {AssertionOperator["=="], AssertionOperator["!="]} and not isinstance(
            assertion_expected, str
        )
        if assertion_operator in numeric_order_operators:
            decimal_value = self._to_decimal(value)
            decimal_expected = self._to_decimal(assertion_expected)
            if decimal_value is not None and decimal_expected is not None:
                value = decimal_value
                assertion_expected = decimal_expected
            elif isinstance(value, (int, float, Decimal)) or isinstance(assertion_expected, (int, float, Decimal)):
                return None
        elif numeric_equality:
            value = self._to_decimal(value)
            expected = self._to_decimal(assertion_expected)
            if value is None or expected is None:
                return None
            assertion_expected = expected
        elif assertion_operator in {AssertionOperator["=="], AssertionOperator["!="]} and not isinstance(value, str):
            expected = self._to_decimal(assertion_expected)
            if expected is not None:
                value = self._to_decimal(value)
                assertion_expected = expected
        return value, assertion_expected

    def _row_matches_assertion(
        self,
        value: Any,
        assertion_operator: AssertionOperator,
        assertion_expected: Any,
    ) -> bool:
        """Evaluate one cell against an assertion, treating missing values and failed assertions as non-matches."""
        value = self.file_reader.convert_missing_values(value)
        if self._is_missing(value):
            return False
        operands = self._coerce_operands(value, assertion_operator, assertion_expected)
        if operands is None:
            return False
        value, assertion_expected = operands

        try:
            verify_assertion(value, assertion_operator, assertion_expected)
        except AssertionError:
            return False
        return True

    def _get_matching_rows(
        self,
        column_assertion: str | int,
        assertion_operator: AssertionOperator,
        assertion_expected: Any,
    ) -> tuple[pd.DataFrame, list[int], bool]:
        """Return the normalized active table, matching row positions, and header-row status."""
        valid_operators = [operator for operator in AssertionOperator if operator != AssertionOperator["then"]]
        if not isinstance(assertion_operator, AssertionOperator) or assertion_operator not in valid_operators:
            raise ValueError(
                f"Unexpected operator for assertion: {assertion_operator}. Use only {[op.value for op in valid_operators]}."
            )

        current_df = self.file_reader.file_sync.table_storage[self.file_reader.file_sync.current_file].data
        table_df, has_header_row = self._prepare_table(current_df)
        column_assertion = self.file_reader.cast_column_type(column_assertion)
        self.file_reader.validate_column(table_df, column_assertion)
        values = (
            table_df.loc[:, column_assertion].to_list()
            if isinstance(column_assertion, str)
            else table_df.iloc[:, column_assertion].to_list()
        )
        matching_rows = [
            row_index
            for row_index, value in enumerate(values)
            if self._row_matches_assertion(value, assertion_operator, assertion_expected)
        ]
        return table_df, matching_rows, has_header_row

    def find_cell_value(
        self,
        column_value: str | int,
        column_assertion: str | int,
        assertion_operator: AssertionOperator,
        assertion_expected: Any,
        return_all: bool = False,
    ) -> Any | list[Any]:
        """Return the first matching cell value or all matching values in table order."""
        table_df, matching_rows, _ = self._get_matching_rows(
            column_assertion,
            assertion_operator,
            assertion_expected,
        )
        column_value = self.file_reader.cast_column_type(column_value)
        self.file_reader.validate_column(table_df, column_value)
        value_column = (
            table_df.loc[:, column_value]
            if isinstance(column_value, str)
            else table_df.iloc[:, column_value]
        )
        values = [
            self.file_reader.convert_missing_values(value)
            for value in value_column.iloc[matching_rows].to_list()
        ]

        if return_all:
            return values
        if not values:
            raise ValueError(
                f"No rows matched the assertion on column '{column_assertion}' "
                f"with operator '{assertion_operator}' and expected value {assertion_expected!r}."
            )
        return values[0]

    def filter_rows(
        self,
        column_assertion: str | int,
        assertion_operator: AssertionOperator,
        assertion_expected: Any,
        return_type: TableFormat = TableFormat["List of lists"],
    ) -> list[list] | list[dict[str, Any]] | pd.DataFrame:
        """Return matching rows in the requested format, preserving applicable header conventions."""
        table_df, matching_rows, has_header_row = self._get_matching_rows(
            column_assertion,
            assertion_operator,
            assertion_expected,
        )
        filtered_df = table_df.iloc[matching_rows]

        if return_type == TableFormat["List of dicts"]:
            return self.file_reader.convert_missing_values(
                cast(list[dict[str, Any]], filtered_df.to_dict(orient="records"))
            )

        if has_header_row:
            filtered_df = pd.DataFrame([table_df.columns.to_list(), *filtered_df.values.tolist()])

        return self.file_reader.convert_dataframe(filtered_df, return_type)
