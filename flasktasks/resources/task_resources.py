from flask import abort
from flask_restful import Resource, reqparse
from loguru import logger

from flasktasks.database.task import TaskRecord, select_all_tasks, select_by_id

task_parser = reqparse.RequestParser()
task_parser.add_argument("title")
task_parser.add_argument("description")
task_parser.add_argument("due_date")


class TaskList(Resource):
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
    def get(self, id: int):
        logger.info(f"Getting task with id {id}")
        if task := select_by_id(id):
            return task.model_dump()
        abort(404, f"Task with ID not found: {id}")
