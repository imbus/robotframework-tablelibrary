from pathlib import Path

class FileSystem:

    def ensure_directory_exists(
            self,
            directory: str
        ) -> bool:
        if directory and not Path(directory).exists():
            Path.mkdir(Path(directory), exist_ok=True)
        return True
