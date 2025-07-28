from robot.api.deco import keyword
from ..general.library_attributes import LibraryAttributes
from ..utils.file_reader import FileReader
from ..utils.settings import FileType


class Getter(LibraryAttributes):

    def __init__(self, library):
        self.library = library
        self.file_reader = FileReader()

    @keyword(tags=["Getter"])
    def get_file_content(self):
        self.file_encoding

    @keyword(tags=["Getter"])
    def get_file_type(self):
        return self.file_type
    
    @keyword(tags=["Getter"])
    def read_table(
            self,
            path: str
        ) -> list:
        """
        Keyword to read the table data for the supported file types.
        """
        self.file_reader.file_exists(path)
        
        if self.file_type == FileType.CSV:
            return self.file_reader.read_csv(path)
        elif self.file_type == FileType.Excel:
            return self.file_reader.read_excel(path)
        elif self.file_type == FileType.Parquet:
            return self.file_reader.read_parquet(path)
        else:
            raise ValueError(f"Not supported data type - file path: {path}")