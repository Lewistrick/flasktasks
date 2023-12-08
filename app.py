from flask import Flask
from flask_restful import Api

from flasktasks.resources import task_resources

app = Flask(__name__)
api = Api(app)

# Add resources for the API. Resources are defined by a resource class and an endpoint.
# A resource class, implements all methods that are allowed, e.g. get().
#
api.add_resource(task_resources.TasksGetter, "/tasks")
api.add_resource(task_resources.TaskGetter, "/task/<int:id>")

if __name__ == "__main__":
    app.run()
