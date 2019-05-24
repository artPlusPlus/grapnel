import pytest

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

        self._on_name_changing()

        original_value = self._name
        self._name = value

        self._on_name_changed(original_value, self._name)

    def __init__(self, name=None):
        super().__init__()

        self._name = None

        self.name = name

    def _on_name_changing(self):
        self.name_changing(self, None)

    def _on_name_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.name_changed(self, data)


def test_hook_existence():
    assert type(Hooked.name_changing) is Hook
    assert type(Hooked.name_changed) is Hook


def test_hook_invocation():
    original_name = "original"
    new_name = "new"

    hooked = Hooked(name=original_name)

    was_invoked = {"changing": False, "changed": False}

    def handle_name_changing(sender, data):
        assert sender is hooked
        assert sender.name == original_name
        was_invoked["changing"] = True

    def handle_name_changed(sender, data):
        assert sender is hooked
        assert sender.name == new_name
        was_invoked["changed"] = True

    hooked.name_changing += handle_name_changing
    hooked.name_changed += handle_name_changed
    hooked.name = new_name

    assert all(was_invoked.values())


def test_hook_not_settable():
    hooked = Hooked(name=None)

    with pytest.raises(ValueError):
        hooked.name_changing = "Foo"


def test_hook_handler_cleanup():
    def handle_name_changing(sender, data):
        pass

    def handle_name_changed(sender, data):
        pass

    hooked = Hooked(name=None)
    hooked.name_changing += handle_name_changing
    hooked.name_changed += handle_name_changed

    assert len(Hooked.name_changing._bound_hooks[hooked]._handler_refs) == 1
    assert len(Hooked.name_changed._bound_hooks[hooked]._handler_refs) == 1

    del handle_name_changing

    assert len(Hooked.name_changing._bound_hooks[hooked]._handler_refs) == 0
    assert len(Hooked.name_changed._bound_hooks[hooked]._handler_refs) == 1

    del handle_name_changed

    assert len(Hooked.name_changing._bound_hooks[hooked]._handler_refs) == 0
    assert len(Hooked.name_changed._bound_hooks[hooked]._handler_refs) == 0
