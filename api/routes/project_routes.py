from flask import Blueprint
from flask_restful import Api
from resources.project_resource import (
    ProjectResource,
    ProjectsByTeamResource,
    ProjectsByUserResource,
    ProjectOverviewResource,
    AddProjectMemberResource,
)

project_blueprint = Blueprint('project', __name__)
project_api = Api(project_blueprint)

project_api.add_resource(ProjectResource, "/projects", "/projects/<int:project_id>")
project_api.add_resource(ProjectsByTeamResource, "/projects/team/<string:team_name>")
project_api.add_resource(ProjectsByUserResource, "/projects/user/<string:username>")
project_api.add_resource(ProjectOverviewResource, "/projects/<int:project_id>/overview")
project_api.add_resource(AddProjectMemberResource, "/projects/<int:project_id>/add-member")