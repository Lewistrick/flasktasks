from flask import abort
from flask_restful import Resource, reqparse
from loguru import logger

from flasktasks.database.task import (
    TaskRecord,
    delete_by_id,
    select_all_tasks,
    select_by_id,
    update_by_id,
)

task_parser = reqparse.RequestParser()
task_parser.add_argument("title")
task_parser.add_argument("description")
task_parser.add_argument("due_date")


class TaskList(Resource):
    """Takes care of reading all tasks and adding tasks."""

    def get(self):
        logger.info("Getting all tasks")
        return [task.model_dump() for task in select_all_tasks()]

    def post(self):
        args = task_parser.parse_args()
        logger.debug(args)
        task = TaskRecord(**args)
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
