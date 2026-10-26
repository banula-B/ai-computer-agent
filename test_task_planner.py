
from src.agent.task_planner import plan_task

command = (
    "Can you please open the notepad and write these two lines: "
    "Hello world, I'm your AI agent"
)

actions = plan_task(command)

for number, action in enumerate(actions, start=1):
    print(f"{number}. {action}")
