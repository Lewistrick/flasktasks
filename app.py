"""The main function for the API.

Can be run with either `flask run` or with `python app.py`.
"""

from flask import Flask
from flask_restful import Api

from flasktasks.resources import home_resources, task_resources

app = Flask(__name__)
api = Api(app)

# Add resources for the API. Resources are defined by a resource class and an endpoint.
# A resource class implements all methods that are allowed, e.g. get() and post().
api.add_resource(home_resources.Help, "/")
api.add_resource(task_resources.TaskList, "/tasklist")
api.add_resource(task_resources.Task, "/task/<int:task_id>")
api.add_resource(task_resources.Search, "/search/<string:query>")

if __name__ == "__main__":
    app.run()
