from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import Tables


class LibraryAttributes:
    def __init__(self, library: "Tables") -> None:
        """
        Expose library attributes to all classes
        """
        self.library = library

    @property
    def file_type(self):
        return self.library._file_type

    @file_type.setter
    def file_type(self, value):
        self.library._file_type = value

    @property
    def separator(self):
        return self.library._separator

    @separator.setter
    def separator(self, value):
        self.library._separator = value

    @property
    def file_encoding(self):
        return self.library._file_encoding

    @file_encoding.setter
    def file_encoding(self, value):
        self.library._file_encoding = value

    @property
    def line_terminator(self):
        return self.library._line_terminator

    @line_terminator.setter
    def line_terminator(self, value):
        self.library._line_terminator = value

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

    @property
    def ignore_header(self):
        return self.library._ignore_header

    @ignore_header.setter
    def ignore_header(self, value):
        self.library._ignore_header = value
