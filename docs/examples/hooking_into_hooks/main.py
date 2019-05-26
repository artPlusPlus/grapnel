from person import Person


def handle_person_name_changing(sender, data):
    assert sender.name == data.current_value
    msg = f"{sender.name} is about to change their name to {data.new_value}."
    print(msg)


def handle_person_name_changed(sender, data):
    assert sender.name == data.current_value
    msg = f"{data.original_value} has changed their name to {data.current_value}."
    print(msg)


def _main():
    person_a = Person(name="Adam")
    person_a.name_changing += handle_person_name_changing
    person_a.name_changed += handle_person_name_changed

    person_b = Person(name="Beth")
    person_b.name_changing += handle_person_name_changing
    person_b.name_changed += handle_person_name_changed

    person_a.name = "Albert"
    person_b.name = "Bonnie"


if __name__ == "__main__":
    _main()
