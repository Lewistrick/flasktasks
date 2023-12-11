from unittest.mock import MagicMock
from pytest import MonkeyPatch, raises
from pytest_mock import MockerFixture

from flasktasks.database.task import (
    TaskRecord,
    search_by_query,
    select_all_tasks,
    select_by_id,
    update_by_id,
)
from flasktasks.tests.mocks import (
    MockQueryResultSet,
    MockSession,
    get_mock_query_result,
    mock_task # noqa
)


def test_get_task(monkeypatch: MonkeyPatch, mocker: MockerFixture):
    mocker.patch("flasktasks.database.task.select")
    mocker.patch("flasktasks.database.task.engine")
    monkeypatch.setattr("flasktasks.database.task.Session", MockSession)
    task = select_by_id(1)
    assert task.task_id == 345
    assert task.title == "test-task"
    assert task.description == ""
    assert task.due_date == "2000-01-01"

def test_get_nonexistent_task(monkeypatch: MonkeyPatch, mocker: MockerFixture):
    mocker.patch("flasktasks.database.task.select")
    mocker.patch("flasktasks.database.task.engine")
    monkeypatch.setattr("flasktasks.database.task.Session", MockSession)
    mocker.patch("flasktasks.tests.mocks.MockQueryResult.first", lambda _: None)
    task = select_by_id(1)
    assert task is None

def test_get_all_tasks(monkeypatch: MonkeyPatch, mocker: MockerFixture):
    mocker.patch("flasktasks.database.task.select")
    mocker.patch("flasktasks.database.task.engine")
    monkeypatch.setattr("flasktasks.database.task.Session", MockSession)
    tasks = select_all_tasks()
    assert all(task.title == "test-task" for task in tasks)
    assert all(task.due_date == f"2000-01-{task.task_id:02d}" for task in tasks)

def test_update_task(monkeypatch: MonkeyPatch, mock_task):
    monkeypatch.setattr("flasktasks.database.task.Session", MockSession)
    new_task = update_by_id(mock_task.task_id, title="new value")
    assert new_task.title == "new value"

def test_update_task_invalid_field(monkeypatch: MonkeyPatch, mocker: MockerFixture):
    monkeypatch.setattr("flasktasks.database.task.Session", MockSession)
    task = TaskRecord(task_id=123, title="", due_date="2000-01-01")
    mocker.patch("flasktasks.database.task.select_by_id", lambda task_id: task)
    with raises(ValueError):
        update_by_id(task.task_id, invalid_field="new value")

def test_search(monkeypatch: MonkeyPatch):
    monkeypatch.setattr("flasktasks.database.task.Session", MockSession)
    monkeypatch.setattr("flasktasks.database.task.select", get_mock_query_result)
    for expected, actual in zip(get_mock_query_result(), search_by_query("test")):
        assert expected == actual

def test_search_sort(monkeypatch: MonkeyPatch, mock_task):
    monkeypatch.setattr("flasktasks.database.task.Session", MockSession)
    monkeypatch.setattr("flasktasks.database.task.select", MockQueryResultSet)
    monkeypatch.setattr("flasktasks.database.task.TaskRecord", mock_task)
    monkeypatch.setattr("flasktasks.database.task.TaskRecord.due_date", MagicMock())
    search_result = search_by_query("test", sort_by="due_date", sort_desc=True)
    for expected, actual in zip(get_mock_query_result(), search_result):
        assert expected == actual