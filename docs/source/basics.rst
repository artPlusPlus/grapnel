Basics
------

Consider a class describing a ``Person``::

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

It would be really valuable if other parts of the code base could hook into instances of ``Person``
and respond when the values of their ``name`` properties change.

In order to use ``Hooks``, they must be imported from Grapnel::

    from grapnel import Hook

Next, two ``Hooks`` are added to ``Person``::

    class Person(object):
        name_changing = Hook()
        name_changed = Hook()

Finally, ``@name.setter`` is modified to invoke the newly added ``Hooks`` just before and after the value of ``name`` is updated::

    @name.setter
    def name(self, value):
        original_value = self._name
        
        self.name_changing(self, (self._name, value))
        self._name = value
        self.name_changed(self, (original_value, self._name))

The full change looks like this::

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