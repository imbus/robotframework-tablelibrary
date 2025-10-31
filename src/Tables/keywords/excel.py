from typing import Any, cast

from pandas import DataFrame
from robot.api import logger
from robot.api.deco import keyword

from ..general.library_attributes import LibraryAttributes
from ..utils.file_reader import FileReader
from ..utils.file_system import FileSync
from ..utils.settings import FileType


class Excel(LibraryAttributes):
    def __init__(self, library):
        self.library = library

        self.df = {}
        self.current_file = None

    ###
    ### Internal Helper Functions
    ###

    @property
    def file_reader(self):
        return FileReader(self.library, FileSync)

    @property
    def data(self) -> DataFrame:
        if not self.df:
            raise ValueError("No file open - use `Excel Open` to read a file first!")
        return self.df

    def _file_type_validation(self):
        if not self.file_type == FileType.Excel:
            raise TypeError(
                f"Wrong file type configuration - actually its '{self.file_type.value}', but expected is '{FileType.Excel.value}'"
            )

    ###
    ### Library Keywords
    ###

    @keyword(tags=["Excel", "Getter"])
    def excel_open(
        self, alias: str, path: str, sheet_name: str | list[str | int] | None = None
    ) -> str:
        """
        Keyword to open the given excel file.

        Opened file will be stored internally & further keywords can be executed to read & validate the excel data from this data.

        | =`Arguments`= | =`Description`= |
        | ``alias`` | Define a alias name to identified the open excel file |
        | ``path`` | Path to the excel file |
        | ``sheet_name`` | Define one or more sheet names to read only specific sheets from the file - default is ``None``to read the complete file |

        == Return Value ==
        Keyword will return the given alias name.

        == Example ==
        | Excel Open    ${directory_to_file}/excel_file.xlsx
        """
        self._file_type_validation()
        self.file_reader.file_exists(path)

        _df = self.file_reader.read_excel(path, sheet_name)
        self.df[alias] = _df
        self.current_file = alias
        return alias

    @keyword(tags=["Excel", "Getter"])
    def excel_close(self, alias: str | None = None) -> bool:
        """
        Keyword to close all or just the given excel file.

        | =`Arguments`= | =`Description`= |
        | ``alias`` | Optional: If given, only the file with this alias is closed. |

        == Example ==
        | ${alias} =    Excel Open    statistics    ${directory_to_file}/excel_file.xlsx
        |
        | Excel Close    ${alias}    # close only one file
        | Excel Close    # close all opened files
        """
        if not self.df:
            logger.info("Nothing to close - no file is opened!")
            return False
        if not alias:
            self.df = {}
            self.current_file = None
            logger.info("Closed all opened excel files!")
            return True
        if alias in self.df:
            del self.df[alias]
            if len(self.df) == 0:
                self.current_file = None
            logger.info(f"Excel file '{alias}' is closed!")
            return True
        raise KeyError(
            f"Given file alias '{alias}' does not exist - check all opened files and their alias first!"
        )

    @keyword(tags=["Excel", "Getter"])
    def excel_get_open_files(self) -> list:
        """
        Keyword returns a list of all currently opened excel files.\n
        It returns the file name alias, defined when the files were opened.

        == Example ==
        | @{files} =    Excel Get Open Files
        """
        files = []
        try:
            for sheet in self.data:
                files.append(sheet)
        except ValueError:
            logger.info("No open file!")
        return files

    @keyword(tags=["Excel", "Getter"])
    def excel_file_switch(self, alias: str):
        """
        Keyword to switch between opened excel files - only if more than one file is opened.

        | =`Arguments`= | =`Description`= |
        | ``alias`` | The defined ``alias`` of the file to switch to. |

        == Example ==
        | Excel File Switch    file_a
        | Excel File Switch    file_b
        """
        if len(self.data) <= 1:
            raise KeyError(
                "No or only one file is opened at the moment - please open at least two excel files to use this keyword!"
            )
        self.current_file = alias

    @keyword(tags=["Excel", "Getter"])
    def excel_sheet_read(self, sheet_name: str) -> list[list[Any]]:
        """
        Keyword to read the data / content of the given ``sheet``.

        The currently opened excel file is taken for reading the data - see ``File Open`` & ``File Switch`` keywords.

        | =`Arguments`= | =`Description`= |
        | ``sheet_name`` | Excel sheet name to read the data from - must be read during file open keyword. |

        == Example ==
        | ${sheet_data} =    Excel Sheet Read    Sheet_Persons
        """
        df = self.data[self.current_file].get(sheet_name)
        if df is None:
            raise ValueError(f"Sheet '{sheet_name}' not found in current file.")
        return cast(list[list[Any]], df.values.tolist())

    @keyword(tags=["Excel", "Getter"])
    def excel_get_available_sheets(self) -> list:
        """
        Keyword returns the available sheets within the currently opened excel file.

        == Example ==
        | @{sheets} =    Excel Get Available Sheets
        """
        return list(self.data[self.current_file].keys())
