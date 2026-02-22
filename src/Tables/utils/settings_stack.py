from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .. import Tables


class Scope(Enum):
    """Some keywords which manipulates library settings have a scope argument.
    With that scope argument one can set the "live time" of that setting.
    Available Scopes are: ``Global``, ``Suite`` and ``Test`` / ``Task``.
    Is a scope finished, this scoped setting, like timeout, will no longer be used
    and the previous higher scope setting applies again.

    Live Times:

    - A ``Global`` scope will live forever until it is overwritten by another Global scope.
      Or locally temporarily overridden by a more narrow scope.
    - A ``Suite`` scope will locally override the Global scope and
      live until the end of the Suite within it is set, or if it is overwritten
      by a later setting with Global or same scope.
      Children suite does inherit the setting from the parent suite but also may have
      its own local Suite setting that then will be inherited to its children suites.
    - A ``Test`` or ``Task`` scope will be inherited from its parent suite but when set,
      lives until the end of that particular test or task.

    A new set higher order scope will always remove the lower order scope which may be in charge.
    So the setting of a Suite scope from a test, will set that scope to the robot file suite where
    that test is and removes the Test scope that may have been in place."""

    Global = auto()
    Suite = auto()
    Test = auto()
    Task = Test


@dataclass
class ScopedSetting:
    typ: Scope
    setting: Any


class SettingsStack:
    def __init__(
        self,
        global_setting: Any,
        ctx: "Tables",
        setter_function: Callable | None = None,
    ):
        self.library = ctx
        self.setter_function = setter_function
        self._stack: dict[str, ScopedSetting] = {"g": ScopedSetting(Scope.Global, global_setting)}

    @property
    def _last_id(self) -> str:
        return list(self._stack.keys())[-1]

    @property
    def _last_setting(self) -> ScopedSetting:
        return list(self._stack.values())[-1]

    def start(self, identifier: str, typ: Scope):
        parent_setting = self._last_setting.setting
        self._stack[identifier] = ScopedSetting(typ, parent_setting)

    def end(self, identifier: str):
        previous = self._stack.pop(identifier, None)
        if previous is not None and self.setter_function is not None and previous != self._last_setting:
            self.setter_function(self._last_setting.setting)

    def set(self, setting: Any, scope: Scope | None = Scope.Global):
        if not self.library.suite_ids:
            scope = Scope.Global
        original = self.get()
        if scope == Scope.Global:
            for value in self._stack.values():
                value.setting = setting
        elif scope == Scope.Suite or scope is None:
            if self._last_setting.typ == Scope.Test:
                self._stack.popitem()
            self._stack[list(self.library.suite_ids)[-1]] = ScopedSetting(Scope.Suite, setting)
        elif scope == Scope.Test:
            if not self.library.is_test_case_running:
                raise ValueError("Setting for test/task can not be set on suite level}")
            current_test_id: str = str(self.library.current_test_id)
            self._stack[current_test_id] = ScopedSetting(Scope.Test, setting)
        else:
            raise ValueError(f"Unknown scope {scope}")
        if self.setter_function and original != setting:
            self.setter_function(setting)
        return original

    def get(self):
        return self._last_setting.setting
