from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import TableLibrary

class LibraryAttributes:
    
    def __init__(self, library: "TableLibrary") -> None:
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
    def delimiter(self):
        return self.library._delimiter

    @property
    def file_encoding(self):
        return self.library._file_encoding

    @property
    def ignore_header(self):
        return self.library._ignore_header