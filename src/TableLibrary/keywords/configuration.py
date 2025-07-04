from ..utils.data_types import *

from robot.api.deco import keyword

class Configuration():

    @keyword(tags=["Configuration"])
    def set_file_type(self, file_type: FileType):
        self.file_type = file_type.value

    @keyword(tags=["Configuration"])
    def set_delimiter(self, file_type: Delimiter):
        self.file_type = file_type.value

    @keyword(tags=["Configuration"])
    def set_file_encoding(self, file_type: FileEncoding):
        self.file_type = file_type.value

    def set_ignore_header(self, ignore_header: bool):
        self.ignore_header = ignore_header