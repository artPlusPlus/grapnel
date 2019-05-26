from typing import Any

from ._base_hook_data import BaseHookData


class ValueChangingHookData(BaseHookData):
    @property
    def current_value(self) -> Any:
        return self._current_value

    @property
    def new_value(self) -> Any:
        return self._new_value

    def __init__(self, current_value: Any, new_value: Any):
        super(ValueChangingHookData, self).__init__()

        self._current_value = current_value
        self._new_value = new_value
