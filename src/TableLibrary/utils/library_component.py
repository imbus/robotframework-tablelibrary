from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from ...TableLibrary import TableLibrary

class LibraryComponent:
    
    def __init__(self, library: "TableLibrary") -> None:
        """Base class exposing attributes from the common context.

        :param library: The library itself as a context object.
        """
        self.library = library
        self._crypto: Optional[Any] = None
        self.browser_arg_mapping: dict[int, str] = {}

    @property
    def file_type(self):
        return self.library._file_type

    @property
    def delimiter(self):
        return self.library._delimiter

    @property
    def file_encoding(self):
        return self.library._file_encoding

    @property
    def ignore_header(self):
        return self.library._ignore_header