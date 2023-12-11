from dataclasses import dataclass

from pytest import MonkeyPatch
from pytest_mock import MockerFixture

from flasktasks.database.task import select_by_id


@dataclass
class MockTaskRecord:
    task_id: int
    title: str
    due_date: str
    description: str = ""

    def create(self):
        return 1


class MockQueryResult:
    def all(self):
        return [
            MockTaskRecord(
                task_id=i,
                title="test-task",
                due_date=f"2000-01-{i:2d}",
            )
            for i in range(3)
        ]

    def first(self):
        return MockTaskRecord(
            task_id=345,
            title="test-task",
            due_date="2000-01-01",
        )


class MockSession:
    def __init__(self, *args, **kwargs):
        pass

    def exec(self, *args, **kwargs):
        return MockQueryResult()

    def __enter__(self):
        return self

    def __exit__(*args, **kwargs):
        pass


def test_get_task(monkeypatch: MonkeyPatch, mocker: MockerFixture):
    mocker.patch("flasktasks.database.task.select")
    mocker.patch("flasktasks.database.task.engine")
    monkeypatch.setattr("flasktasks.database.task.Session", MockSession)
    task = select_by_id(1)
    assert task.task_id == 345
    assert task.title == "test-task"
    assert task.description == ""
    assert task.due_date == "2000-01-01"
