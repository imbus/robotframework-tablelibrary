from pathlib import Path

class FileSystem:

    def ensure_directory_exists(
            self,
            directory: Path
        ) -> bool:
        if directory and not directory.exists():
            Path.mkdir(directory, exist_ok=True)
        return True

class FileSync:
    def __init__(self):
        self.current_file: Path = None
