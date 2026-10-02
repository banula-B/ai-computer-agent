from agent.commands import execute_command


print("Computer Agent started.")

while True:
    command = input("What should I do? ")

    if command.lower().strip() == "exit":
        print("Computer Agent stopped.")
        break

    execute_command(command)