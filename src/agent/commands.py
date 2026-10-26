
import re

from computer.applications import open_application
from computer.keyboard import type_text, press_key


def normalize_command(command):
    command = command.lower().strip()
    command = command.rstrip(".!?,")

    # Remove common polite phrases.
    command = re.sub(
        r"^(please\s+|can you\s+|could you\s+|"
        r"would you\s+|hey computer\s+)+",
        "",
        command
    )

    # Correct common Whisper transcription errors.
    corrections = {
        "node pad": "notepad",
        "note pad": "notepad",
        "not panned": "notepad",
        "not bad": "notepad",
        "not pan": "notepad",
        "calculator app": "calculator",
        "ms paint": "paint",
    }

    command = re.sub(r"^right(?=\s)", "write", command)

    for wrong, correct in corrections.items():
        command = command.replace(wrong, correct)

    return command.strip()


def execute_command(command):
    command = normalize_command(command)

    print(f"Executing command: {command}")

    # Exit
    if command in ("exit", "quit", "stop agent", "close agent"):
        return "exit"

    # Open applications
    app_commands = {
        "notepad": ("notepad", ["notepad"]),
        "calculator": ("calculator", ["calculator", "calc"]),
        "paint": ("mspaint", ["paint", "mspaint"]),
    }

    for app_name, (executable, aliases) in app_commands.items():
        for alias in aliases:
            if command in (
                f"open {alias}",
                f"launch {alias}",
                f"start {alias}"
            ):
                open_application(executable)
                print(f"Opened {app_name}.")
                return

    # Write or type text
    for prefix in ("write ", "type ", "write down ", "enter text "):
        if command.startswith(prefix):
            text = command[len(prefix):].strip()

            if text:
                type_text(text)
            else:
                print("No text provided.")

            return

    # Keyboard commands
    key_commands = {
        "press enter": "enter",
        "hit enter": "enter",
        "press space": "space",
        "hit space": "space",
        "press backspace": "backspace",
        "hit backspace": "backspace",
        "press tab": "tab",
        "hit tab": "tab",
    }

    if command in key_commands:
        press_key(key_commands[command])
        return

    print(f"Unknown command: {command}")
