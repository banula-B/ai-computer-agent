
import re

from agent.task_planner import plan_task
from computer.applications import open_application
from computer.keyboard import type_text, press_key


def normalize_command(command):
    command = command.lower().strip()
    command = command.rstrip(".!?,")

    command = re.sub(
        r"^(please\s+|can you\s+|could you\s+|"
        r"would you\s+|hey computer\s+)+",
        "",
        command,
    )

    corrections = {
        "node pad": "notepad",
        "north pad": "notepad",
        "northpad": "notepad",
        "note pad": "notepad",
        "not panned": "notepad",
        "not bad": "notepad",
        "not pan": "notepad",
        "calculator app": "calculator",
        "ms paint": "paint",
    }

    for wrong, correct in corrections.items():
        command = command.replace(wrong, correct)

    command = re.sub(r"^right(?=\s)", "write", command)

    return command.strip()


def execute_action(action):
    action_type = action["action"]

    if action_type == "open_app":
        open_application(action["app"])
        print(f"Opened {action['app']}.")

    elif action_type == "write_text":
        type_text(action["text"])

    elif action_type == "press_key":
        press_key(action["key"])

    else:
        print(f"Unsupported action: {action_type}")



def execute_command(command):
    original_command = command.strip()
    normalized_command = normalize_command(original_command)

    print(f"Executing command: {normalized_command}")

    if normalized_command in ("exit", "quit", "stop agent", "close agent"):
        return "exit"

    # Plan using the original transcription to preserve text capitalization.
    actions = plan_task(original_command)

    if actions:
        print(f"Task plan contains {len(actions)} actions.")

        for number, action in enumerate(actions, start=1):
            print(f"Executing action {number}: {action}")
            execute_action(action)

        print("Task execution finished.")
        return

    # Use normalized text for the existing single-command handlers.
    command = normalized_command

    # Preserve support for the existing single-app commands.
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
                f"start {alias}",
            ):
                open_application(executable)
                print(f"Opened {app_name}.")
                return

    # Preserve existing text-entry commands.
    for prefix in ("write ", "type ", "write down ", "enter text "):
        if command.startswith(prefix):
            text = command[len(prefix):].strip()

            if text:
                type_text(text)
            else:
                print("No text provided.")

            return

    # Preserve existing keyboard commands.
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
