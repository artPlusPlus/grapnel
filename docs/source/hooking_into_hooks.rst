Hooking into Hooks
------------------

Once a class has implemented ``Hooks``, external code can be notified by adding callbacks.

Start by creating two handlers; one for each ``Hook`` that was added to ``Person``::

    def handle_person_name_changing(sender, data):
        assert sender.name == data.current_value
        msg = f'{sender.name} is about to change their name to {data.new_value}'.

    def handle_person_name_changed(sender, data):
        assert sender.name == data.current_value
        msg = f'{data.original_value} has changed their name to {data.current_value}'.

.. warning:: Handlers must accept two arguments:

  - ``sender``: The instance which invoked the ``Hook``.
  - ``data``: Additional data about whatever is happening. While this can be anything, it recommended that
    a ``HookData`` class be used.

Now, any time a ``Person`` instance is created, the ``+=`` operator can be used to attach a handler to the instance's ``Hook``::

    a_person = Person()
    a_person.name_changing += handle_person_name_changing
    a_person.name_changed += handle_person_name_changed

And that's it. Anytime ``a_person.name`` changes (and only when the value will _actually_ change),
``handle_person_name_changing`` and ``handle_person_name_changed`` will be called.