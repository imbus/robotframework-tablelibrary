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
    def ignore_header(self):
        return self.library._ignore_header

    @ignore_header.setter
    def ignore_header(self, value):
        self.library._ignore_header = value
