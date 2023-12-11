from flask_restful import Resource
from loguru import logger


class Help(Resource):
    """Takes care of reading all tasks and adding tasks."""

    def get(self):
        logger.info("Showing index")
        return {
            "message": "This is the home page of Flasktasks, a REST API for a task list.",
            "What can you do where": {
                "See all tasks": {
                    "endpoint": "/tasklist",
                    "method": "GET",
                },
                "See one task": {
                    "endpoint": "/task/<task_id>",
                    "method": "GET",
                },
                "Create a task": {
                    "endpoint": "/tasklist",
                    "method": "POST",
                    "body": [
                        {
                            "name": "title",
                            "required": True,
                            "type": "string",
                        },
                        {
                            "name": "description",
                            "required": False,
                            "type": "string",
                        },
                        {
                            "name": "due_date",
                            "required": True,
                            "type": "string",
                            "comment": "format should be yyyy-mm-dd",
                        },
                    ],
                },
                "Delete a task": {"endpoint": "/task/<task_id>", "method": "DELETE"},
                "Edit a task": {
                    "endpoint": "/task/<task_id> {[title], [description], [due_date]}",
                    "method": "PUT",
                    "body": [
                        {
                            "name": "title",
                            "required": False,
                            "type": "string",
                        },
                        {
                            "name": "description",
                            "required": False,
                            "type": "string",
                        },
                        {
                            "name": "due_date",
                            "required": False,
                            "type": "string",
                            "comment": "format should be yyyy-mm-dd",
                        },
                    ],
                },
                "Search for tasks": {
                    "endpoint": "/search/<search_query>",
                    "method": "GET",
                },
            },
        }
