import pytest

from Tables.keywords.getter import Getter

from .helper.helpers import DummyLibrary


@pytest.fixture
def getter():
    # LibraryAttributes expects a parent library, wir nutzen Dummy
    return Getter(DummyLibrary())


# ToDO
