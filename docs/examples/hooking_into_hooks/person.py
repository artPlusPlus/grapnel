from grapnel import Hook, ValueChangingHookData, ValueChangedHookData


class Person:
    name_changing = Hook()
    name_changed = Hook()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            value = None
        if value == self._name:
            return

        original_value = self._name
        self._on_name_changing(self._name, value)
        self._name = value
        self._on_name_changed(original_value, self._name)

    def __init__(self, name=None):
        super().__init__()

        self._name = None
        self.name = name

    def _on_name_changing(self, current_value, new_value):
        data = ValueChangingHookData(current_value, new_value)
        self.name_changing(self, data)

    def _on_name_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.name_changed(self, data)
