from computer.applications import open_application
from computer.keyboard import type_text, press_key


def execute_command(command):
    command = command.strip()

    if command.lower() == "open notepad":
        open_application("notepad")

    elif command.lower() == "open calculator":
        open_application("calculator")

    elif command.lower() == "open paint":
        open_application("mspaint")

    elif command.lower().startswith("write "):
        text = command[6:]
        type_text(text)

    elif command.lower() == "press enter":
        press_key("enter")

    else:
        print("I don't know how to perform that command.")