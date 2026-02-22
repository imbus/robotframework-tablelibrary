"""Shared test helpers.

The production library (`Tables`) uses a scope-aware `SettingsStack` to manage
settings such as `ignore_header`. For unit tests we often don't have a running
Robot Framework execution context (suite/test ids), but `SettingsStack` still
expects a context object exposing a few attributes.

`DummyLibrary` implements the minimal subset of the `Tables` API required by
`LibraryAttributes` / `SettingsStack`.
"""

from __future__ import annotations

from Tables.utils.settings import (
    Delimiter,
    FileEncoding,
    FileType,
    LineTerminator,
    Quoting,
    QuotingCharacter,
)
from Tables.utils.settings_stack import SettingsStack


class DummyLibrary:
    def __init__(self, *, ignore_header: bool = False):
        # configuration attributes used by LibraryAttributes
        self._quoting = Quoting.MINIMAL
        self._quoting_character = QuotingCharacter['"']

        # attributes expected by SettingsStack
        self.scope_stack: dict = {}
        self.suite_ids: dict[str, None] = {}
        self.current_test_id: str | None = None
        self.is_test_case_running: bool = False

        self.scope_stack["ignore_header"] = SettingsStack(ignore_header, self)
        self.scope_stack["file_type"] = SettingsStack(FileType.CSV, self)
        self.scope_stack["separator"] = SettingsStack(Delimiter[","], self)
        self.scope_stack["line_terminator"] = SettingsStack(LineTerminator.LF, self)
        self.scope_stack["file_encoding"] = SettingsStack(FileEncoding.UTF_8.value, self)
