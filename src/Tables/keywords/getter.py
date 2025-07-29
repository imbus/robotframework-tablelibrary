from robot.api.deco import keyword
from ..general.library_attributes import LibraryAttributes
from ..utils.file_reader import FileReader
from ..utils.settings import FileType
from typing import Any


class Getter(LibraryAttributes):

    def __init__(self, library):
        self.library = library
        self.file_reader = FileReader(library)

    @keyword(tags=["Getter"])
    def get_file_content(self):
        return self.file_encoding.value

    @keyword(tags=["Getter"])
    def get_file_type(self):
        return self.file_type.value

    @keyword(tags=["Getter"])
    def read_table(
            self,
            path: str
        ) -> Any:
        """
        Keyword to read the table data for the supported file types.
        """
        self.file_reader.file_exists(path)

        if self.file_type == FileType.CSV:
            return self.file_reader.read_csv(path)
        if self.file_type == FileType.Excel:
            return self.file_reader.read_excel(path)
        if self.file_type == FileType.Parquet:
            return self.file_reader.read_parquet(path)
        raise ValueError(f"Not supported data type - file path: {path}")
