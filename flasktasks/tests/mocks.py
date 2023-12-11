from dataclasses import dataclass
from unittest.mock import MagicMock
import pytest


def get_mock_query_result(*args, **kwargs):
    return [
        MockTaskRecord(task_id=i, title="test-task", due_date=f"2000-01-{i:02d}")
        for i in range(3)
    ]

class MockQueryResultSet:
    def __init__(self, *args, **kwargs):
        self.records: list[MockTaskRecord] = get_mock_query_result()
        self._desc = False

    def order_by(self, column):
        if column._desc:
            return self.records[::-1]
        return self.records

class MockColumn:
    def __init__(self, column_name):
        self.name = column_name
        self.desc = False
    
    def desc(self):
        self._desc = True
    


@dataclass
class MockTaskRecord:
    task_id: int | None
    title: str
    due_date: str
    description: str | None = ""

    def create(self):
        return self.task_id

    def model_dump(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "due_date": self.due_date,
            "description": self.description
        }
    
    def model_validate(*args, **kwargs):
        pass




class MockQueryResult:
    def __init__(self, *args, **kwargs):
        pass

    def all(self, *args, **kwargs):
        return get_mock_query_result()

    def first(self):
        return MockTaskRecord(
            task_id=345,
            title="test-task",
            due_date="2000-01-01",
        )
    
    def yield_per(self, *args, **kwargs):
        return self.all()


class MockSession:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def add(self, *args, **kwargs):
        pass

    def commit(self):
        pass

    def exec(self, *args, **kwargs):
        return MockQueryResult(*args, **kwargs)

    def refresh(self, *args, **kwargs):
        pass

class MockSelector():
    def __init__(self):
        self.call_count = 0

    def __call__(self):
        self.call_count += 1
        return [MockTaskRecord(task_id=123, title="test", due_date="2000-01-01")]
    
class MockRequest:
    args = {}


@pytest.fixture
def mock_task():
    return MockTaskRecord(
        task_id=123,
        title="test-task",
        due_date="2000-01-01",
    )

@pytest.fixture
def mock_selector():
    return MockSelector()
