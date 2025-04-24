import json
from pathlib import Path
import pytest
from pytest_mock import MockerFixture
from app.main import load_tasks, DATA_FILE




def test_load_tasks_file_exists(mocker: MockerFixture):
    """
    Test case for the `load_tasks` function to verify behavior when the tasks file exists.

    This test uses mocking to simulate the presence of a tasks file and its content.
    It ensures that the `load_tasks` function correctly reads and returns the tasks
    from the file.

    Args:
        mocker (MockerFixture): A pytest-mock fixture used to mock dependencies.

    Mocks:
        - `builtins.open`: Simulates opening a file and reading JSON data.
        - `pathlib.Path.exists`: Simulates the existence of the tasks file.

    Asserts:
        - The returned tasks from `load_tasks` match the mocked tasks data.
    """
    mock_tasks = [{"description": "Test task"}]
    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps(mock_tasks)))
    mocker.patch("pathlib.Path.exists", return_value=True)

    tasks = load_tasks()
    assert tasks == mock_tasks


def test_load_tasks_file_not_exists(mocker: MockerFixture):
    """
    Test case for the `load_tasks` function to verify behavior when the tasks file does not exist.

    This test uses mocking to simulate the absence of a tasks file. It ensures that the
    `load_tasks` function returns an empty list when the file is not found.

    Args:
        mocker (MockerFixture): A pytest-mock fixture used to mock dependencies.

    Mocks:
        - `pathlib.Path.exists`: Simulates the absence of the tasks file.

    Asserts:
        - The returned tasks from `load_tasks` are an empty list.
    """
    mocker.patch("pathlib.Path.exists", return_value=False)

    tasks = load_tasks()
    assert tasks == []
