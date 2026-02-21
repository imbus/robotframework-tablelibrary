import pytest

from Tables.utils.settings_stack import Scope, SettingsStack

from .helper.helpers import DummyLibrary


@pytest.fixture
def ctx() -> DummyLibrary:
    return DummyLibrary()


def test_get_returns_global_setting_on_init(ctx: DummyLibrary):
    stack = SettingsStack("g0", ctx)
    assert stack.get() == "g0"


def test_start_inherits_parent_setting(ctx: DummyLibrary):
    stack = SettingsStack("g0", ctx)
    stack.start("suite1", Scope.Suite)

    assert stack.get() == "g0"
    assert stack._stack["suite1"].typ == Scope.Suite
    assert stack._stack["suite1"].setting == "g0"


def test_set_global_updates_all_existing_stack_entries_and_calls_setter(ctx: DummyLibrary):
    setter_calls: list[str] = []
    stack = SettingsStack("g0", ctx, setter_calls.append)
    stack.start("suite1", Scope.Suite)
    stack.start("test1", Scope.Test)

    original = stack.set("g1", Scope.Global)

    assert original == "g0"
    assert stack.get() == "g1"
    assert {v.setting for v in stack._stack.values()} == {"g1"}
    assert setter_calls == ["g1"]


def test_set_suite_overrides_current_scope_and_end_reverts_to_previous_value(ctx: DummyLibrary):
    ctx.suite_ids = {"suite1": None}
    setter_calls: list[str] = []
    stack = SettingsStack("g0", ctx, setter_calls.append)

    stack.start("suite1", Scope.Suite)
    assert stack.get() == "g0"

    original = stack.set("s1", Scope.Suite)
    assert original == "g0"
    assert stack.get() == "s1"
    assert setter_calls == ["s1"]

    stack.end("suite1")
    assert stack.get() == "g0"
    assert setter_calls == ["s1", "g0"]


def test_set_suite_from_test_scope_removes_test_scope(ctx: DummyLibrary):
    ctx.suite_ids = {"suite1": None}
    ctx.is_test_case_running = True
    ctx.current_test_id = "t1"
    setter_calls: list[str] = []

    stack = SettingsStack("g0", ctx, setter_calls.append)
    stack.start("suite1", Scope.Suite)
    stack.start("t1", Scope.Test)

    stack.set("tv", Scope.Test)
    assert stack.get() == "tv"

    original = stack.set("sv", Scope.Suite)
    assert original == "tv"
    assert stack.get() == "sv"
    assert "t1" not in stack._stack
    assert stack._stack["suite1"].typ == Scope.Suite
    assert setter_calls == ["tv", "sv"]


def test_set_scope_none_is_treated_as_suite(ctx: DummyLibrary):
    ctx.suite_ids = {"suite1": None}
    stack = SettingsStack("g0", ctx)
    stack.start("suite1", Scope.Suite)

    stack.set("s1", None)
    assert stack.get() == "s1"


def test_set_test_scope_requires_running_test(ctx: DummyLibrary):
    ctx.suite_ids = {"suite1": None}
    ctx.is_test_case_running = False
    ctx.current_test_id = "t1"
    stack = SettingsStack("g0", ctx)

    with pytest.raises(ValueError, match="can not be set on suite level"):
        stack.set("tv", Scope.Test)


def test_set_forces_global_if_no_suite_ids_even_if_suite_scope_requested(ctx: DummyLibrary):
    # without any suite context, SettingsStack treats all settings as global
    ctx.suite_ids = {}
    setter_calls: list[str] = []
    stack = SettingsStack("g0", ctx, setter_calls.append)
    stack.start("suite1", Scope.Suite)

    stack.set("g1", Scope.Suite)
    assert {v.setting for v in stack._stack.values()} == {"g1"}
    assert setter_calls == ["g1"]


def test_end_calls_setter_only_if_setting_changes(ctx: DummyLibrary):
    setter_calls: list[str] = []
    stack = SettingsStack("g0", ctx, setter_calls.append)

    # if we start another Global scope, it is equal to the previous entry
    # and ending it should not trigger a setter call.
    stack.start("g2", Scope.Global)
    stack.end("g2")
    assert setter_calls == []
