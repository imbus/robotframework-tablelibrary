from ..utils.file_reader import FileReader
from ..utils.file_system import FileSync
from ..utils.file_writer import FileWriter


class FileAccess:
    def __init__(self, library):
        shared_file_sync = FileSync()

        self.file_reader = FileReader(library, shared_file_sync)
        self.file_writer = FileWriter(library, shared_file_sync)
