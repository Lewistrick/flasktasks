from flask import Flask
from flask_restful import Api

from flasktasks.resources import task_resources

app = Flask(__name__)
api = Api(app)

api.add_resource(task_resources.TaskGetter, "/task/<int:id>")

if __name__ == "__main__":
    app.run()
