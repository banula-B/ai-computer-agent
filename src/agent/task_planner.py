
import re


def plan_task(command):
    command = command.strip()

    # Remove polite introductory phrases.
    command = re.sub(
        r"^(?:(?:hey computer|can you please|could you please|"
        r"would you please|can you|could you|please)\s+)+",
        "",
        command,
        flags=re.IGNORECASE,
    ).strip()

    # Correct common speech-recognition errors.
    command = re.sub(
        r"\b(?:north pad|note pad|node pad|not bad|not panned|not pan)\b",
        "notepad",
        command,
        flags=re.IGNORECASE,
    )
    command = re.sub(
        r"^right(?=\s)",
        "write",
        command,
        flags=re.IGNORECASE,
    )

    actions = []

    # Identify the application-opening instruction.
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

    # Find an explicit two-line instruction.
    two_lines_match = re.search(
        r"\b(?:write|type|write down|enter text)\s+"
        r"(?:these|the following)\s+two lines\b"
        r"\s*[:,?.!]?\s*(.*)",
        command,
        flags=re.IGNORECASE,
    )

    if two_lines_match:
        text = two_lines_match.group(1).strip()
        if "," in text:
            parts = [part.strip() for part in text.split(",", 1)]
        else:
            parts = re.split(r"\s+\band\b\s+", text, maxsplit=1, flags=re.IGNORECASE)
            parts = [part.strip() for part in parts]

        if len(parts) == 2 and all(parts):
            actions.extend([
                {"action": "write_text", "text": parts[0]},
                {"action": "press_key", "key": "enter"},
                {"action": "write_text", "text": parts[1]},
            ])
        else:
            print(
                "I couldn't confidently identify both lines. "
                "Please separate the two lines with a comma."
            )
            return []

        return actions

    # Handle ordinary write/type instructions.
    write_match = re.search(
        r"\b(?:write down|write|type|enter text)\s+(.+)",
        command,
        flags=re.IGNORECASE,
    )

    if write_match:
        text = write_match.group(1).strip()

        # Do not type fragments of an unfinished instruction.
        incomplete_phrases = {
            "down",
            "these two lines",
            "the following two lines",
        }

        if text.lower().strip(" .?!,") in incomplete_phrases:
            print("Incomplete instruction. Please repeat the full request.")
            return []

        text = re.sub(r"[.!?]+$", "", text).strip()

        if text:
            actions.append({
                "action": "write_text",
                "text": text,
            })

    return actions
