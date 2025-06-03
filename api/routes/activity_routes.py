from flask import Blueprint
from flask_restful import Api
from resources.activity_resource import (
    TaskActivityResource,
    ProjectActivityResource,
)

activity_blueprint = Blueprint('activity', __name__)
activity_api = Api(activity_blueprint)

activity_api.add_resource(TaskActivityResource, "/task/activity/<int:task_id>")
activity_api.add_resource(ProjectActivityResource, "/projects/activity/<int:project_id>")