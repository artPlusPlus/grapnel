from grapnel import Hook


class Door(object):
    opened = Hook()
    closed = Hook()

    @property
    def name(self):
        return self._name

    @property
    def is_open(self):
        return self._is_open

    def __init__(self, name, is_open=False):
        super().__init__()

        self._name = name
        self._is_open = is_open

    def open(self):
        if self.is_open:
            return

        self._is_open = True
        self.opened(self, None)

    def close(self):
        if not self.is_open:
            return

        self._is_open = False
        self.closed(self, None)


def handle_door_opened(sender, data):
    msg = f"The {sender.name} door has opened!"
    print(msg)


def handle_door_closed(sender, data):
    msg = f"The {sender.name} door has closed."
    print(msg)


def _main():
    front_door = Door("Front")
    front_door.opened += handle_door_opened
    front_door.closed += handle_door_closed

    back_door = Door("Back")
    back_door.opened += handle_door_opened
    back_door.closed += handle_door_closed

    front_door.open()
    front_door.close()

    back_door.open()
    back_door.close()


if __name__ == "__main__":
    _main()
