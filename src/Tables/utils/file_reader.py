from ..general.library_attributes import LibraryAttributes

import csv
import pandas as pd
from pathlib import Path
from typing import Any, cast


class FileReader(LibraryAttributes):
    def __init__(self, library):
        super().__init__(library)

    def file_exists(self, path: str) -> bool | FileNotFoundError:
        if not Path(path).is_file():
            raise FileNotFoundError(f"File not found: {path}")
        return True

    def read_csv(self, path: str) -> list[list[Any]]:
        with Path(path).open(mode="r", newline="", encoding=self.file_encoding.value) as f:
            rows = list(csv.reader(f, delimiter=self.delimiter.value))
            if self.ignore_header:
                return rows[1:]
            return rows

    def read_excel(self, path: str) -> list[list[Any]]:
        header = 0 if self.ignore_header else None
        df = pd.read_excel(path, header=header)
        return cast(list[list[Any]], df.values.tolist())

    def read_parquet(self, path: str) -> Any:
        df = pd.read_parquet(path)
        data = df.values.tolist()
        if not self.ignore_header:
            data.insert(0, list(df.columns))
        return data
