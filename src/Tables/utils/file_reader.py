from ..general.library_attributes import LibraryAttributes

import os
import csv
import pandas as pd

class FileReader(LibraryAttributes):

    def __init__(self, library):
        super().__init__(library)

    def file_exists(
            self,
            path: str
        ) -> bool | FileNotFoundError:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File not found: {path}")
        return True

    def read_csv(
            self,
            path: str
        ) -> list:
        with open(path, newline='', encoding=self.file_encoding.value) as f:
            reader = csv.reader(f, delimiter=self.delimiter.value)
            rows = [row for row in reader]
            if self.ignore_header:
                return rows[1:]
            return rows

    def read_excel(
            self,
            path: str
        ) -> list:
        header = 0 if self.ignore_header else None
        df = pd.read_excel(path, header=header)
        return df.values.tolist()
    
    def read_parquet(
            self,
            path: str
        ) -> list:
        df = pd.read_parquet(path)
        data = df.values.tolist()
        if not self.ignore_header:
            data.insert(0, list(df.columns))
        return data