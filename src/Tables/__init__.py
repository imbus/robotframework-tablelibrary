# SPDX-FileCopyrightText: 2025-present Marvin Klerx <marvinklerx20@gmail.com>
#
# SPDX-License-Identifier: MIT
from robot import result, running
from robot.api.deco import library
from robotlibcore import HybridCore

from Tables.utils.settings_stack import Scope, SettingsStack

from .__about__ import __version__
from .keywords import (
    Configuration,
    Getter,
    Modifier,
    # Excel
    Writer,
)
from .utils.file_access import FileAccess
from .utils.settings import (
    Delimiter,
    FileEncoding,
    FileType,
    LineTerminator,
    Quoting,
    QuotingCharacter,
)


@library(scope="GLOBAL", version=__version__)
class Tables(HybridCore):
    """
    ``TableLibrary`` is a generic automation library for working with files like csv, parquet, etc.

    == Table of content ==

    %TOC%

    == Supported File Types ==
    - CSV
    - Excel
    - Parquet
    - TXT -> will be interpreted as CSV file
    - More coming soon...

    == Supported File Encoding ==
    - utf-8
    - utf-16
    - latin-1
    - further more... (define your own file encoding with the given library argument)

    == Live Data Streaming ==
    Some keywords allow you to write the inserted or appended data directly into an output table file.
    By default, the table library writes the modified table data first into the internal cache.
    In this case, you decide when to write the data into a file.

    If you require the modified data on the fly within the file on your file system, you can enable the streaming via ``Configure Streaming``.

    Afterwards, every keyword that allows the on-the-fly streaming, writes the new data directly into the file system instead of modifying the table just in the cache.

    Example:
    |  # enable the streaming on-the-fly
    |  Configure Streaming    True    Test
    |
    |  VAR    ${filepath} =    ${CURDIR}/results/test_writer_live_streaming_append_row.csv
    |  VAR    @{headers} =    counter    random
    |  ${uuid} =    Tables.Create Table    headers=${headers}    file_path=${filepath}
    |
    |  # append ten rows on-the-fly within the given csv file
    |  FOR    ${i}    IN RANGE    ${10}
    |      ${random} =    Generate Random String    10
    |      VAR    @{row} =    ${i}    ${random}
    |      Tables.Append Row    ${row}
    |
    |      ${table_content} =    Tables.Read Table    ${filepath}
    |      Should Be Equal    ${table_content}[-1][1]    ${random}
    |  END

    == Excel Files ==
    We have included a basic handling of ``Excel`` files,
    but for more complex excel features, please take a look at the following library:
    [https://pypi.org/project/robotframework-excelsage|robotframework-excelsage].
    \nThis library got especially written to work with Excel files, sheets, etc...

    == Examples ==
    === File Format - CSV ===
    | # Reading CSV file with header column
    | ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    | ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "index"
    | BuiltIn.Should Be True    ${result}
    |
    |
    | # Reading CSV file without header column
    | Tables.Configure Ignore Header    True
    | ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_01.csv
    | ${result} =    BuiltIn.Evaluate    "index" not in "${content}"
    | BuiltIn.Should Be True    ${result}

    === File Format - Parquet ===
    | Tables.Configure File Type    Parquet
    | ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_05.parquet
    | ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "_time"
    | BuiltIn.Should Be True    ${result}

    === Create new empty table - don't save to file system ===
    | # Create some data which should be inserted into the new table
    | VAR    @{headers} =    name    age
    | VAR    @{person1} =    Michael    34
    | VAR    @{person2} =    John    19
    |
    | # Create empty table object - internally in cache
    | ${uuid} =    Tables.Create Table    headers=${headers}
    |
    | # Append some rows
    | Tables.Append Row    ${person1}
    | Tables.Append Row    ${person2}
    | Count Table    ${uuid}    Rows    equal    ${3}
    |
    | # Append a column
    | VAR    @{column1} =    city    MG    ERL
    | Tables.Append Column    ${column1}
    | Count Table    ${uuid}    Columns    equal    ${3}
    |
    | # Optional: Set new table cell value
    | Get Table Cell    1    1    equals    34
    | Tables.Set Table Cell    25    0    1
    | Get Table Cell    1    1    equals    25
    |
    | # Insert a new row into the existing table object
    | VAR    @{insert_row} =    Lu    26    Hamburg
    | Insert Row    ${insert_row}    0
    | Get Table Cell    1    0    equals    Lu
    | Count Table    ${uuid}    Rows    equal    ${4}

    === Create new empty table - save to file system ===
    | # Generate new headers which should be used in the table
    | VAR    @{headers} =    name    age
    |
    | # Create new table object
    | ${uuid} =    Create Table    ${headers}
    |
    | # Generate some random data & append as rows to new table
    | FOR    ${_}    IN RANGE    ${100}
    |     ${a} =    Generate Random String
    |     ${b} =    Generate Random String
    |     VAR    @{data}    ${a}    ${b}
    |     Tables.Append Row    ${data}
    | END
    |
    | # Ensure that data got written into internal table object
    | Count Table    ${uuid}    Rows    equals    ${101}
    |
    | # Write table to specific file path -> write from cache into persistant file
    | Write Table    ${uuid}    ${CURDIR}/results/test_writer_new_table.csv
    |
    | # Check table content again, but now read table from file path!
    | Count Table    ${CURDIR}/results/test_writer_new_table.csv    Rows    equals    ${101}

    === Parquet ===
    | Tables.Configure File Type    Parquet
    | ${content} =    Tables.Read Table    ${CURDIR}${/}testdata${/}example_05.parquet
    | ${result} =    BuiltIn.Evaluate    "${content}[0][0]" == "_time"
    | BuiltIn.Should Be True    ${result}
    """

    def __init__(  # noqa: PLR0913
        self,
        *,
        file_type: FileType = FileType.CSV,
        file_encoding: FileEncoding | str = FileEncoding.UTF_8,
        separator: Delimiter = Delimiter[","],
        ignore_header: bool = False,
        line_terminator: LineTerminator = LineTerminator.LF,
        quoting: Quoting = Quoting.MINIMAL,
        quoting_character: QuotingCharacter = QuotingCharacter['"'],
    ):
        """
        ``TableLibrary`` can be controlled by the following arguments:

        | =`Argument`=      | =`Description`= |
        | ``file_type``     | Choose the file type to test initially. |
        | ``file_encoding`` | Defiine the file encoding - select from given hints or define your own by string value. |
        | ``separator``     | Define a separator for parsing the files. |
        | ``ignore_header`` | Define if headers in files should be ignored. Default is ``False``  |
        | ``line_terminator`` | Define the required line terminator for your table files. Default is ``False``  |
        | ``quoting`` | Define which values should be surrounded with quotes, please check the CSV quoting for more details. Default is ``MINIMAL``  |
        | ``quoting_character`` | Define quoting character to use for writing table files. Default is ``\"``  |
        """

        # required variables for SettingsScope mechanism
        self.scope_stack: dict = {}
        self.suite_ids: dict[str, None] = {}
        self.current_test_id: str | None = None
        self.is_test_case_running = False

        # following config variables are using SettingsStack engine with scopes
        self.scope_stack["ignore_header"] = SettingsStack(ignore_header, self)
        self.scope_stack["file_type"] = SettingsStack(file_type, self)
        self.scope_stack["separator"] = SettingsStack(separator, self)
        self.scope_stack["line_terminator"] = SettingsStack(line_terminator, self)
        self.scope_stack["file_encoding"] = SettingsStack(
            file_encoding.value if isinstance(file_encoding, FileEncoding) else file_encoding, self
        )
        self.scope_stack["quoting"] = SettingsStack(quoting, self)
        self.scope_stack["quoting_character"] = SettingsStack(quoting_character, self)
        self.scope_stack["enable_streaming"] = SettingsStack(False, self)

        self.file_access = FileAccess(self)

        self.ROBOT_LIBRARY_LISTENER = [
            self,
            Modifier(self, self.file_access),
        ]

        libraries = [
            Configuration(self),
            Getter(self, self.file_access),
            Writer(self, self.file_access),
            Modifier(self, self.file_access),
            # Excel(self)
        ]

        super().__init__(libraries)

    def _start_suite(self, _name: running.TestSuite, attrs: result.TestSuite):
        self.suite_ids[attrs.id] = None
        self._add_to_scope_stack(attrs.id, Scope.Suite)

    def _start_test(self, _name: running.TestCase, attrs: result.TestCase):
        self.current_test_id = attrs.id
        self._add_to_scope_stack(attrs.id, Scope.Test)
        self.is_test_case_running = True

    def _end_test(self, _name: running.TestCase, attrs: result.TestCase):
        self._remove_from_scope_stack(attrs.id)
        self.current_test_id = None
        self.is_test_case_running = False

    def _end_suite(self, _name: running.TestSuite, attrs: result.TestSuite):
        self._remove_from_scope_stack(attrs.id)
        self.suite_ids.pop(attrs.id, None)

    def _add_to_scope_stack(self, scope_id: str, scope: Scope):
        for stack in self.scope_stack.values():
            stack.start(scope_id, scope)

    def _remove_from_scope_stack(self, scope_id):
        for stack in self.scope_stack.values():
            stack.end(scope_id)
