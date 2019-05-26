******************
Hooking into Hooks
******************

Once a class has implemented ``Hooks``, handlers can be created and attached. When a hook is 
invoked, all handlers attached to the hook will be called in the order in which they were attached.

.. literalinclude:: ../examples/hooking_into_hooks/main.py
    :language: python
    :linenos:
    :emphasize-lines: 4-7, 10-13, 18-19, 22-23

.. warning:: Handlers must accept two arguments: ``sender`` and ``data``.

  - ``sender``: The instance which invoked the ``Hook``.
  - ``data``: Additional data about whatever is happening. While this can be anything, it recommended that
    a ``HookData`` class be used.

And that's it. Anytime ``a_person.name`` changes, ``handle_person_name_changing`` and
``handle_person_name_changed`` will be called.