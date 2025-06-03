from flask import Blueprint
from flask_restful import Api
from resources.task_resource import (
    TaskResource,
    TasksByProjectResource,
    TasksBySprintResource,
    TasksByUserResource,
)


task_blueprint = Blueprint('task', __name__)
task_api = Api(task_blueprint)

task_api.add_resource(TaskResource, "/tasks", "/tasks/<int:task_id>")
task_api.add_resource(TasksByProjectResource, "/tasks/project/<int:project_id>")
task_api.add_resource(TasksBySprintResource, "/tasks/sprint/<int:sprint_id>")
task_api.add_resource(TasksByUserResource, "/users/<string:username>/tasks")