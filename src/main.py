from agent.commands import execute_command
from voice.speech_to_text import listen


print("Computer Agent started.")

while True:

    command = listen()

    if command is None:
        continue

    result = execute_command(command)

    if result == "exit":
        print("Computer Agent stopped.")
        break