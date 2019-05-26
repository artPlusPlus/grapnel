from Grapnel import Hook


class Person(object):
    name_changing = Hook()
    name_changed = Hook()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        original_value = self._name

        self.name_changing(self, (self._name, value))
        self._name = value
        self.name_changed(self, (original_value, self._name))

    def __init__(self, name=None):
        super().__init__()

        self._name = name
