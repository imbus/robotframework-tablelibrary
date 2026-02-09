import importlib


def test_keywords_init_exports():
    module = importlib.import_module("Tables.keywords")
    exported = set(module.__all__)
    assert {"Configuration", "Excel", "Getter", "Modifier", "Writer"} <= exported
