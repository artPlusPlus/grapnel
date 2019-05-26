Recommendations
---------------

While the ``Person`` class we ended up with at the end of the `Basics` section is funtional,
there are a few things that can be done to tighten it up a bit.

Let's step back to the original ``Person`` definition::

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

Similar to before, Grapnel is imported and the ``Person`` class exposes two ``Hook`` instances: ``name_changing`` and ``name_changed``::

    from grapnel import Hook

    class Person():
        name_changing = Hook()
        name_changed = Hook()

Next, ``@name.setter`` is modified to invoke the ``Hooks``, but with some slight differences::

    @name.setter
    def name(self, value):
        if not value:
            value = None
        if value == self._name:
            return
        
        original_value = self._name

        self._on_name_changing()
        self._name = value
        self._on_name_changed(original_value, self._name)

  - ``value == self._name`` has been added to ensure the ``Hooks`` are invoked only when the value actually changes.
  - Instead of invoking the ``Hooks`` directly, two private methods are called: ``self._on_name_changing()`` and ``self._on_name_changed``.

Then, the ``_on_name_changing()`` and ``_on_name_changed()`` methods are implemented::

    def _on_name_changing(self, current_value, new_value):
        data = ValueChangingHookData(current_value, new_value)
        self.name_changing(self, data)

    def _on_name_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.name_changed(self, data)

Before examining the benefits of these methods, the imports must be updated::

    from grapnel import Hook, ValueChangingHookData, ValueChangedHookData

So, why bother with encapsulating the ``Hook`` invokations?

  - Instead of passing raw data to handlers (as tuples, in the Simple Usage example), state-change data can be pre-processed and packaged up into something a bit more ergonomic.
  - While not required in this example, it is likely that a single aspect of an object instance's
    state can change in multiple places throughout the object's implementation. Encapsulating data pre-processing and ``Hook`` invokation can increase maintainability.


The final Person class should look like this::

    from grapnel import Hook, ValueChangingHookData, ValueChangedHookData

    class Person():
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
            self._on_name_changing()
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
