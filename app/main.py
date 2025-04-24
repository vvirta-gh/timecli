import argparse
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if DATA_FILE.exists():
            with open(DATA_FILE, "r") as f:
                return json.load(f)
            return []
        return []
    
    def save_tasks(self):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump(self.tasks, f, indent=2)
        return None
    
    def add_task(self, description):
        self.tasks.append({"description": description})
        self.save_tasks()
        print(f"Added task: {description}")
        return None
    
    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
        else:
            for idx, task in enumerate(self.tasks, 1):
                print(f"{idx}. {task['description']}")
        return None
    
    

def main():
    parser = argparse.ArgumentParser(description="Task Manager")
    subparsers = parser.add_subparsers(dest="command")
    task_manager = TaskManager()
    
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    list_parser = subparsers.add_parser("list", help="List all tasks")
    args = parser.parse_args()
    
    if args.command == "add":
        task_manager.add_task(args.description)
    elif args.command == "list":
        task_manager.list_tasks()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
