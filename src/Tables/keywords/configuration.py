from ..utils.settings import FileEncoding, FileType, Delimiter
from ..general.library_attributes import LibraryAttributes

from robot.api.deco import keyword

class Configuration(LibraryAttributes):

    @keyword(tags=["Configuration"])
    def configure_file_type(self, file_type: FileType):
        """
        Change the internal file type during your test execution dynamically.
        """
        self.file_type = file_type

    @keyword(tags=["Configuration"])
    def configure_delimiter(self, delimiter: Delimiter):
        """
        Change the internal delimiter during your test execution dynamically.
        """
        self.delimiter = delimiter

    @keyword(tags=["Configuration"])
    def configure_file_encoding(self, file_encoding: FileEncoding):
        """
        Change the internal file encoding during your test execution dynamically.
        """
        self.file_encoding = file_encoding

    @keyword(tags=["Configuration"])
    def configure_ignore_header(self, ignore_header: bool):
        """
        Change the internal setting to (not) ignore the data header lines during your test execution dynamically.
        """
        self.ignore_header = ignore_header