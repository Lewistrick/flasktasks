from flask import abort
from flask_restful import Resource
from loguru import logger

from flasktasks.database.task import select_all_tasks, select_by_id


class TasksGetter(Resource):
    def get(self):
        logger.info("Getting all tasks")
        return [task.model_dump() for task in select_all_tasks()]


class TaskGetter(Resource):
    def get(self, id: int):
        logger.info(f"Getting task with id {id}")
        if task := select_by_id(id):
            return task.model_dump()
        abort(404, f"Task with ID not found: {id}")
