from robot.api.deco import keyword
from ..general.library_attributes import LibraryAttributes
from ..utils.settings import FileType
from ..utils.file_system import FileSystem

from typing import Any
import pandas as pd
from pathlib import Path

class Writer(LibraryAttributes):

    def __init__(self, library):
        self.library = library

    @property
    def _fs(self):
        return FileSystem()

    @keyword(tags=['Writer'])
    def write_table(
            self,
            data: list[list[Any]],
            file_path: str
        ) -> str:
        """
        Keyword to write the given data to a new file.

        | =`Arguments`= | =`Description`= |
        | ``data`` | Data object to store in a new file |
        | ``file_path`` | The full path of your file system to store the file. |

        == Example ==
        | Write Table    ${data}    ${CURDIR}/output/statistics.csv
        """
        dir_name = Path(file_path).parent
        self._fs.ensure_directory_exists(dir_name)

        if not self.ignore_header:
            headers = data[0]
            rows = data[1:]
            df = pd.DataFrame(rows, columns=headers)
        else:
            df = pd.DataFrame(data)

        writers = {
            FileType.CSV: lambda: df.to_csv(file_path, index=False),
            FileType.Excel: lambda: df.to_excel(file_path, index=False),
            FileType.Parquet: lambda: df.to_parquet(file_path, index=False)
        }

        writer = writers.get(self.file_type)
        if writer:
            writer()
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
        return file_path

    @keyword(tags=["Writer"])
    def write_cell(
            self,
            alias: str,
            row: int,
            column: int
        ) -> list[list[Any]]:
        """
        Keyword to (over-) write the value of a specific cell.
        """
        return [[None]]

    @keyword(tags=["Writer"])
    def write_column(
            self,
            alias: str,
            column: int
        ) -> list[list[Any]]:
        return [[None]]

    @keyword(tags=["Writer"])
    def write_row(
            self,
            alias: str,
            row: int,
        ) -> list[list[Any]]:
        return [[None]]
