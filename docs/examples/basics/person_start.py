class Person(object):
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def __init__(self, name=None):
        super().__init__()

        self._name = name
