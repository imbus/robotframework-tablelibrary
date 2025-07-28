from ..general.library_attributes import LibraryAttributes

import os
import csv
import pandas as pd

class FileReader(LibraryAttributes):

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
        with open(path, newline='', encoding=self.file_encoding) as f:
            reader = csv.reader(f)
            return [row for row in reader]

    def read_excel(
            self,
            path: str
        ) -> list:
        df = pd.read_excel(path, header=None)
        return df.values.tolist()
    
    def read_parquet(
            self,
            path: str
        ) -> list:
        df = pd.read_parquet(path)
        return df.values.tolist()