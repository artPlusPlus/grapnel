from grapnel import Hook, ValueChangedHookData


class Hooked(object):
    name_changing = Hook()
    name_changed = Hook()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value == self._name:
            return
        elif not value:
            value = None

    def _on_name_changing(self):
        self.name_changing(self, None)

    def _on_name_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.name_changed(self, data)


def test_hook_existence():
    assert type(Hooked.name_changing) is Hook
    assert type(Hooked.name_changed) is Hook
