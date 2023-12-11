from typing import Mapping

from flask import abort, request
from flask_restful import Resource, reqparse
from loguru import logger

from flasktasks.config import settings
from flasktasks.database.task import (
    TaskRecord,
    delete_by_id,
    search_by_query,
    select_all_tasks,
    select_by_id,
    update_by_id,
)

task_parser = reqparse.RequestParser()
task_parser.add_argument("title")
task_parser.add_argument("description")
task_parser.add_argument("due_date")


def paginate[T](elements: list[T], params: Mapping[str, str]) -> list[T]:
    """Given a list of elements, return page `from_idx` for page size `page_size`.

    The typehints use Python3.12's new typevar syntax.
    In practice, this means this function is dependent on some type T that is unknown,
    but `elements` is a list of this type,
    and the return type is also a list of this type as well.
    """
    page_from = int(params.get("page", 1))
    page_size = int(params.get("per", settings.page_size))

    page = elements[(page_from - 1) * page_size : page_from * page_size]
    return page


class TaskList(Resource):
    """Takes care of reading all tasks and adding tasks."""

    def get(self):
        """Get all tasks.

        Supports pagination: use GET parameters `page` and `per` to specify the page
        number and the page size, e.g. /tasks?page=2&per=5.
        """
        logger.info("Getting all tasks")

        all_tasks = [task.model_dump() for task in select_all_tasks()]

        return paginate(all_tasks, request.args)

class TaskCreate(Resource):
    def post(self):
        """Create a new task."""
        args = task_parser.parse_args()
        logger.debug(args)
        task = TaskRecord(**args)
        logger.debug("Creating task")
        task_id = task.create()
        return {
            "message": "task created succesfully",
            "id": task_id,
            **task.model_dump(),
        }


class Task(Resource):
    """Takes care of operations done on an existing task.

    GET reads a task;
    PUT edits a task;
    DELETE removes a task.
    """

    def get(self, task_id: int):
        logger.info(f"Getting task with {task_id=}")
        if task := select_by_id(task_id):
            return task.model_dump()
        abort(404, f"Task with ID not found: {task_id}")

    def delete(self, task_id: int):
        logger.info(f"Deleting task with {task_id=}")
        if delete_by_id(task_id):
            return {"message": "task deleted succesfully", "id": task_id}
        abort(404, f"Task with {task_id=} can't be deleted, because it doesn't exist")

    def put(self, task_id: int):
        """Edit a task with given ID.

        The attributes to edit are in the request body. Attributes that are not
        specified will not be changed.
        """
        args = {
            attr: value
            for attr, value in task_parser.parse_args().items()
            if value is not None
        }
        task = update_by_id(task_id, **args)
        if task is not None:
            return {
                "message": "task updated succesfully",
                "id": task_id,
                **task.model_dump(),
            }
        abort(404, f"Task with {task_id=} can't be updated, because it doesn't exist")


class Search(Resource):
    def get(self, query: str):
        """Search for tasks given a query.

        Here, the GET method was chosen because the queries are simple text.
        For more complex search, one might want to use POST.

        Supports sorting: use GET parameters `sort` and `desc` to specify sorting, e.g.
            /tasks/search/query?sort=due_date&desc=1
        to sort by due_date, newest first.

        Supports pagination: use GET parameters `page` and `per` to specify the page
        number and the page size, e.g.
            /tasks/search/query?page=2&per=10
        to show results 11 through 20.
        """
        logger.info(f"Searching tasks by text: {query}")
        sort_by = request.args.get("sort")
        sort_desc = bool(request.args.get("desc", False))
        search_result = [
            task.model_dump() for task in search_by_query(query, sort_by, sort_desc)
        ]
        return paginate(search_result, request.args)
