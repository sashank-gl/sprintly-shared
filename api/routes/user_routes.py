from flask import Blueprint
from flask_restful import Api
from resources.user_resource import (
    UserResource,
    UserAvatarResource,
    TeamMembersResource, AllUsersResource
)


user_blueprint = Blueprint('user', __name__)
user_api = Api(user_blueprint)

user_api.add_resource(UserResource, '/users/<int:user_id>')
user_api.add_resource(UserAvatarResource, '/users/<int:user_id>/avatar')
user_api.add_resource(TeamMembersResource, '/teams/<string:team>/members')
user_api.add_resource(AllUsersResource, '/users')