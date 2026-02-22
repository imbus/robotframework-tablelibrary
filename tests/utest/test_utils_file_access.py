from Tables.utils.file_access import FileAccess

from .helper.helpers import DummyLibrary


def test_file_access_shares_sync_between_reader_and_writer():
    access = FileAccess(DummyLibrary())
    assert access.file_reader.file_sync is access.file_writer.file_sync
