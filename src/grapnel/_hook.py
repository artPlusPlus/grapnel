from __future__ import annotations

import weakref

from typing import Any, Callable, Union, List


class BoundHook(object):
    """
    `BoundHook`s associate callbacks with specific object instances.
    """

    @property
    def _default_data_value(self):
        if isinstance(self._default_data_value_ref, weakref.ReferenceType):
            return self._default_data_value_ref()
        return self._default_data_value_ref

    @_default_data_value.setter
    def _default_data_value(self, value):
        try:
            self._default_data_value_ref = weakref.WeakMethod(value)
        except TypeError:
            try:
                self._default_data_value_ref = weakref.ref(value)
            except TypeError:
                self._default_data_value_ref = value

    def __init__(self, default_data_value: Any):
        super(BoundHook, self).__init__()

        self._default_data_value_ref = None
        self._handler_refs: List[Union[weakref.ReferenceType, weakref.WeakMethod]] = []

        self._default_data_value = default_data_value

    def add_handler(self, handler: Callable[[Any, Any], None]) -> None:
        """
        Adds a handler to the Hook.

        When a ``BoundHook`` is invoked, handlers are called in the order in which they were added.
        ``BoundHook`` holds only weak references to handlers. Manual cleanup due to handler 
        lifespan should not be necessary.
        """
        handler_ref = self._create_handler_ref(handler)
        if not handler_ref:
            msg = "Failed to add handler: Unable to create weak reference."
            raise ValueError(msg)

        self._handler_refs.append(handler_ref)

    def remove_handler(self, handler: Callable[[Any, Any], None]) -> None:
        """
        Removes a handler from the Hook.

        ``BoundHook`` holds only weak references to handlers. Manual cleanup due to handler 
        lifespan should not be necessary.
        """
        handler_ref = self._create_handler_ref(handler)
        if not handler_ref:
            return

        self._handler_refs.remove(handler_ref)

    def __call__(self, sender: Any, data: Any = None) -> None:
        if data is None:
            data = self._default_data_value

        for handler_ref in self._handler_refs:
            handler = handler_ref()
            if handler:
                handler(sender, data)

    def __iadd__(self, handler: Callable) -> BoundHook:
        self.add_handler(handler)
        return self

    def __isub__(self, handler: Callable) -> BoundHook:
        self.remove_handler(handler)
        return self

    def _create_handler_ref(self, handler):
        try:
            result = weakref.WeakMethod(handler, self._handler_ref_died)
        except TypeError:
            try:
                result = weakref.ref(handler, self._handler_ref_died)
            except TypeError:
                result = None

        return result

    def _handler_ref_died(self, handler_ref):
        try:
            self._handler_refs.remove(handler_ref)
        except ValueError:
            pass


class Hook(object):
    """
    `Hook`s are the primary feature of Grapnel.

    `Hook`s are class-level constructs. A class can have any number of `Hook`s.

    Once a class exposes a `Hook`, callbacks can be attached to the `Hook` via instances
    of the class.
    """

    def __init__(self, default_data_value: Any = None):
        """
        Initializes a new `Hook` instance.

        Args:
            default_data_value: In the case where a `Hook` is invoked with no data, this value will
                be passed to any attached callbacks.
        """
        super(Hook, self).__init__()

        self._bound_hooks: weakref.WeakKeyDictionary[Any, BoundHook] = weakref.WeakKeyDictionary()
        self._default_data_value = default_data_value

    def __get__(self, instance, owner=None):
        if instance is None:
            return self

        try:
            result = self._bound_hooks[instance]
        except KeyError:
            result = BoundHook(self._default_data_value)
            self._bound_hooks[instance] = result

        return result

    def __set__(self, instance, value):
        if self._bound_hooks.get(instance) is value:
            return
        raise ValueError(
            "Hooks cannot be set. Use the '+=' operator to assign a callback to the hook."
        )
