import tempfile
import json
from pathlib import Path
from app.taskmanager import TaskManager

def test_add_and_list_tasks(capsys):
    # Create temporary file
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpfile = Path(tmpdirname) / "tasks.json"
        
        # Create TaskManager by using this file
        manager = TaskManager(data_file=tmpfile)
        
        manager.add_task("Testitehtävä on tämä")
        
        with open(tmpfile, "r") as f:
            data = json.load(f)
        
        assert data == [{"description": "Testitehtävä on tämä"}]
        
        # Test that list_tasks() prints correctly
        manager.list_tasks()
        captured = capsys.readouterr()
        assert "1. Testitehtävä on tämä" in captured.out