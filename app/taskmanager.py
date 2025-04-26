from pathlib import Path
import json

class TaskManager:
    def __init__(self, data_file=None):
        self.data_file = data_file or (Path(__file__).parent.parent / "data" / "tasks.json")
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if self.data_file.exists():
            with open(self.data_file, "r") as f:
                return json.load(f)
            return []
        return []
    
    def save_tasks(self):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, "w") as f:
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