from computer.applications import open_application
from computer.keyboard import type_text, press_key


def execute_command(command):

    # Clean the command
    command = command.strip()
    command = command.rstrip(".!?")

    # Remove commas after command words
    command = command.replace(",", "", 1)

    command_lower = command.lower()

    # -------------------------
    # Exit
    # -------------------------
    if command_lower == "exit":
        return "exit"

    # -------------------------
    # Open applications
    # -------------------------
    if command_lower == "open notepad":
        open_application("notepad")
        return

    if command_lower == "open calculator":
        open_application("calculator")
        return

    if command_lower == "open paint":
        open_application("mspaint")
        return

    # -------------------------
    # Write / Type text
    # -------------------------
    if command_lower.startswith("write "):
        text = command[6:].strip()
        type_text(text)
        return

    if command_lower.startswith("type "):
        text = command[5:].strip()
        type_text(text)
        return

    # Whisper sometimes hears "write" as "right"
    if command_lower.startswith("right "):
        text = command[6:].strip()
        type_text(text)
        return

    # -------------------------
    # Keyboard
    # -------------------------
    if command_lower == "press enter":
        press_key("enter")
        return

    if command_lower == "press space":
        press_key("space")
        return

    if command_lower == "press backspace":
        press_key("backspace")
        return

    # -------------------------
    # Unknown command
    # -------------------------
    print(f"I don't know how to perform that command.")