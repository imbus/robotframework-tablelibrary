from dataclasses import dataclass
from pathlib import Path

from pandas import DataFrame


@dataclass
class TableObject:
    path: Path
    data: DataFrame


class FileSystem:
    def ensure_directory_exists(self, directory: Path) -> bool:
        if directory and not directory.exists():
            Path.mkdir(directory, exist_ok=True)
        return True


class FileSync:
    def __init__(self) -> None:
        self.table_storage: dict[str, TableObject] = {}
        self.current_file: str | None = None
