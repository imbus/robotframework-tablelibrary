from robot.api.deco import keyword
from ..general.library_attributes import LibraryAttributes


class Getter(LibraryAttributes):

    @keyword(tags=["Getter"])
    def get_file_content(self):
        self.file_encoding

    @keyword(tags=["Getter"])
    def get_file_type(self):
        return self.file_type