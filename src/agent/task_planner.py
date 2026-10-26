
import re


def plan_task(command):
    """
    Convert a natural-language instruction into ordered actions.

    Supported in this first version:
    - Open Notepad, Calculator, or Paint.
    - Write one line of text.
    - Write two lines when explicitly requested.
    """

    command = command.strip()

    # Remove polite phrases without changing the text's capitalization.
    command = re.sub(
        r"^(?:(?:hey computer|can you please|could you please|"
        r"would you please|can you|could you|please)\s+)+",
        "",
        command,
        flags=re.IGNORECASE,
    ).strip()

    # Correct a common Whisper transcription error.
    command = re.sub(
        r"^right(?=\s)",
        "write",
        command,
        flags=re.IGNORECASE,
    )

    actions = []

    # Find an application to open.
    app_match = re.search(
        r"\b(?:open|launch|start)\s+(?:the\s+)?"
        r"(notepad|calculator|paint)\b",
        command,
        flags=re.IGNORECASE,
    )

    if app_match:
        app = app_match.group(1).lower()

        executables = {
            "notepad": "notepad",
            "calculator": "calculator",
            "paint": "mspaint",
        }

        actions.append({
            "action": "open_app",
            "app": executables[app],
        })

    # Find the text the user wants to write.
    write_match = re.search(
        r"\b(?:write|type|write down|enter text)\s+(.+)",
        command,
        flags=re.IGNORECASE,
    )

    if write_match:
        text = write_match.group(1).strip()

        # Remove ending punctuation from the instruction.
        text = re.sub(r"[.!?]+$", "", text).strip()

        # Handle an explicit request for two lines.
        two_lines = re.match(
            r"^(?:these two lines|the following two lines)"
            r"\s*[:,?.!]?\s*(.+)$",
            text,
            flags=re.IGNORECASE,
        )

        if two_lines:
            text = two_lines.group(1).strip()
            lines = [line.strip() for line in text.split(",", 1)]

            if len(lines) == 2 and all(lines):
                actions.append({
                    "action": "write_text",
                    "text": lines[0],
                })
                actions.append({
                    "action": "press_key",
                    "key": "enter",
                })
                actions.append({
                    "action": "write_text",
                    "text": lines[1],
                })
            else:
                actions.append({
                    "action": "write_text",
                    "text": text,
                })
        else:
            actions.append({
                "action": "write_text",
                "text": text,
            })

    return actions
