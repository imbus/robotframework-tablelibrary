from typing import TYPE_CHECKING

from Tables.utils.settings import Delimiter, FileType, LineTerminator
from Tables.utils.settings_stack import SettingsStack

if TYPE_CHECKING:
    from .. import Tables


class LibraryAttributes:
    def __init__(self, library: "Tables") -> None:
        """
        Expose library attributes to all classes
        """
        self.library = library

    @property
    def quoting(self):
        return self.library._quoting

    @quoting.setter
    def quoting(self, value):
        self.library._quoting = value

    @property
    def quoting_character(self):
        return self.library._quoting_character

    @quoting_character.setter
    def quoting_character(self, value):
        self.library._quoting_character = value

    ###
    ### New strategy: use SettingsStack like in Browser library for different scopes
    ###

    # ignore_header
    @property
    def ignore_header(self) -> bool:
        return self.library.scope_stack["ignore_header"].get()

    @property
    def ignore_header_stack(self) -> SettingsStack:
        return self.library.scope_stack["ignore_header"]

    @ignore_header_stack.setter
    def ignore_header_stack(self, stack: SettingsStack):
        self.library.scope_stack["ignore_header"] = stack

    # file_type
    @property
    def file_type(self) -> FileType:
        return self.library.scope_stack["file_type"].get()

    @property
    def file_type_stack(self) -> SettingsStack:
        return self.library.scope_stack["file_type"]

    @file_type_stack.setter
    def file_type_stack(self, stack: SettingsStack):
        self.library.scope_stack["file_type"] = stack

    # separator / delimiter
    @property
    def separator(self) -> Delimiter:
        return self.library.scope_stack["separator"].get()

    @property
    def separator_stack(self) -> SettingsStack:
        return self.library.scope_stack["separator"]

    @separator_stack.setter
    def separator_stack(self, stack: SettingsStack):
        self.library.scope_stack["separator"] = stack

    # line terminator
    @property
    def line_terminator(self) -> LineTerminator:
        return self.library.scope_stack["line_terminator"].get()

    @property
    def line_terminator_stack(self) -> SettingsStack:
        return self.library.scope_stack["line_terminator"]

    @line_terminator_stack.setter
    def line_terminator_stack(self, stack: SettingsStack):
        self.library.scope_stack["line_terminator"] = stack

    # file encoding
    @property
    def file_encoding(self) -> LineTerminator:
        return self.library.scope_stack["file_encoding"].get()

    @property
    def file_encoding_stack(self) -> SettingsStack:
        return self.library.scope_stack["file_encoding"]

    @file_encoding_stack.setter
    def file_encoding_stack(self, stack: SettingsStack):
        self.library.scope_stack["file_encoding"] = stack
