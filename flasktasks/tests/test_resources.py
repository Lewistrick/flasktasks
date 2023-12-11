from unittest.mock import MagicMock

from pytest import MonkeyPatch, raises
from pytest_mock import MockerFixture

from flasktasks.resources.helpers import paginate
from flasktasks.resources.task_resources import TaskList
from flasktasks.tests.mocks import MockRequest, mock_selector


def test_paginate():
    """Test if pagination works, using ranges"""
    page = paginate(list(range(10)), params={"page": 2, "size": 5})
    assert page == list(range(5, 10))

def test_get_all(monkeypatch: MonkeyPatch, mocker: MockerFixture, mock_selector):
    monkeypatch.setattr("flasktasks.resources.task_resources.request", MockRequest)
    monkeypatch.setattr("flasktasks.resources.task_resources.select_all_tasks", mock_selector)
    mocker.patch("flasktasks.resources.helpers.paginate")

    TaskList().get()
    assert mock_selector.call_count == 1