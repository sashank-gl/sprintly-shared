from flask_restful import Resource
from models.activity import Activity
from models.user import User
from app import db


class TaskActivityResource(Resource):
    def get(self, task_id):
        activities = db.session.query(Activity, User).join(User, Activity.actor == User.username).filter(Activity.task_id == task_id).order_by(Activity.timestamp.desc()).all()

        return [
            {
                "actor": a.actor,
                "actor_name": f"{u.first_name} {u.last_name}",
                "action": a.action,
                "field_changed": a.field_changed,
                "old_value": a.old_value,
                "new_value": a.new_value,
                "timestamp": a.timestamp.isoformat() + "Z",
                "task_id": a.task_id,
                "project_id": a.project_id
            }
            for a, u in activities
        ]
    
class ProjectActivityResource(Resource):
    def get(self, project_id):
        activities = db.session.query(Activity, User).join(User, Activity.actor == User.username).filter(Activity.project_id == project_id).order_by(Activity.timestamp.desc()).all()

        return [
            {
                "actor": a.actor,
                "actor_name": f"{u.first_name} {u.last_name}",
                "action": a.action,
                "item_type": a.item_type,
                "item_id": a.item_id,
                "field_changed": a.field_changed,
                "old_value": a.old_value,
                "new_value": a.new_value,
                "timestamp": a.timestamp.isoformat() + "Z",
                "task_id": a.task_id,
                "project_id": a.project_id
            }
            for a, u in activities
        ]