from flask import request
from flask_restful import Resource
from services.user_service import get_user, update_avatar, remove_avatar
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg'}
UPLOAD_FOLDER = 'static/avatars'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class UserResource(Resource):
    def get(self, user_id):
        user = get_user(user_id)

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "job_title": getattr(user, "job_title", None),
            "team": getattr(user, "team", None),
            "role": getattr(user, "role", None),
            "avatar_url": user.avatar_url,
        }, 200


class UserAvatarResource(Resource):
    def put(self, user_id):
        if 'avatar' not in request.files:
            return {"message": "No file provided"}, 400
        file = request.files['avatar']
        if file.filename == '':
            return {"message": "No selected file"}, 400
        if file and allowed_file(file.filename):
            file.seek(0, os.SEEK_END)
            file_length = file.tell()
            file.seek(0)
            max_size = 500 * 1024
            if file_length > max_size:
                return {"message": "File too large. Max size is 500KB"}, 400
            filename = secure_filename(file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            avatar_url = f"/{filepath}"
            user = update_avatar(user_id, avatar_url)
            return {"avatar_url": user.avatar_url}, 200
        return {"message": "Invalid file type"}, 400
    
    def delete(self, user_id):
        user = remove_avatar(user_id)
        return {"message": "Avatar removed"}, 200
    

class TeamMembersResource(Resource):
    def get(self, team):
        from models.user import User
        users = User.query.filter_by(team=team).all()
        return [
            {
                "id": u.id,
                "username": u.username,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "email": u.email,
                "job_title": u.job_title,
                "role": u.role,
                "team": u.team,
            }
            for u in users
        ], 200
    
    
class AllUsersResource(Resource):
    def get(self):
        from models.user import User
        users = User.query.all()
        return [
            {
                "id": u.id,
                "username": u.username,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "email": u.email,
                "job_title": u.job_title,
                "role": u.role,
                "team": u.team,
            }
            for u in users
        ], 200