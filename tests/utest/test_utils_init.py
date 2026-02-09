import importlib


def test_utils_init_module_imports():
    module = importlib.import_module("Tables.utils")
    assert module is not None
