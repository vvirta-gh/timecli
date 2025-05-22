import argparse
import json
from pathlib import Path
from app.taskmanager import TaskManager

def cli():
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
    cli()
