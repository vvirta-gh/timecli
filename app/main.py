import argparse
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "tasks.json"


def load_tasks():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    return []


def save_tasks(tasks):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

    return None


def add_task(description):
    tasks = load_tasks()
    tasks.append({"description": description})
    save_tasks(tasks)
    print(f"Added task: {description}")

    return None


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
    else:
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task['description']}")

    return None


def main():
    parser = argparse.ArgumentParser(description="Task Manager")
    subparsers = parser.add_subparsers(dest="command")

    # Create a subparser for the 'add' command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    subparsers.add_parser("list", help="List all tasks")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
