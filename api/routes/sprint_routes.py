from flask import Blueprint
from flask_restful import Api
from resources.sprint_resource import SprintResource

sprint_blueprint = Blueprint('sprint', __name__)
sprint_api = Api(sprint_blueprint)

sprint_api.add_resource(SprintResource, "/sprints", "/sprints/<int:sprint_id>")