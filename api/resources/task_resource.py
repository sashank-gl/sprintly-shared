from flask_restful import Resource, reqparse
from services.task_service import create_task, update_task
from models.task import Task
from models.user import User
from models.project import Project
from models.sprint import Sprint
from extensions import db

class TaskResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", required=True)
        parser.add_argument("description", required=False)
        parser.add_argument("status", required=True)
        parser.add_argument("priority", required=True)
        parser.add_argument("type", required=True)
        parser.add_argument("scope", required=True)
        parser.add_argument("tool", required=True)
        parser.add_argument("due_date", required=False)
        parser.add_argument("project_id", type=int, required=True)
        parser.add_argument("sprint_id", type=int, required=False)
        parser.add_argument("owner_id", type=int, required=False)
        parser.add_argument("created_by", type=str, required=True)
        args = parser.parse_args()

        task = create_task(args, actor=args["created_by"])
        return {
            "message": "Task created successfully",
            "task_id": task.id,
            "task_title": task.title
        }, 201
    

    def get(self, task_id):
        from models.task import Task
        task = Task.query.get_or_404(task_id)

        return {
            "id": task.id,
            "task_id": f"Task-{task.id if task.id >= 1000 else str(task.id).zfill(3)}",
            "title": task.title,
            "description": task.description or [],
            "status": task.status,
            "priority": task.priority,
            "type": task.type,
            "scope": task.scope,
            "tool": task.tool,
            "due_date": task.due_date.isoformat() + "Z" if task.due_date else None,
            "created_date": task.created_date.isoformat() + "Z" if task.created_date else None,
            "completed_date": task.completed_date.isoformat() + "Z" if task.completed_date else None,
            "last_updated_date": task.last_updated_date.isoformat() + "Z" if task.last_updated_date else None,
            "sprint_id": task.sprint_id,
            "sprint_name": Sprint.query.get(task.sprint_id).name if task.sprint_id else None,
            "project_id": task.project_id,
            "project_name": Project.query.get(task.project_id).name if task.project_id else None,
            "owner_id": task.owner_id,
            "owner_name": f"{User.query.get(task.owner_id).first_name} {User.query.get(task.owner_id).last_name}" if task.owner_id else None,
            "created_by": task.created_by,
            "created_by_name": f"{User.query.filter_by(username=task.created_by).first().first_name} {User.query.filter_by(username=task.created_by).first().last_name}" if task.created_by else None,
        }
    

    def put(self, task_id):
        parser = reqparse.RequestParser()
        parser.add_argument("title")
        parser.add_argument("description", type=list, location='json')
        parser.add_argument("status")
        parser.add_argument("priority")
        parser.add_argument("type")
        parser.add_argument("scope")
        parser.add_argument("tool")
        parser.add_argument("due_date")
        parser.add_argument("sprint_id", type=int)
        parser.add_argument("owner_id", type=str)
        parser.add_argument("updated_by", type=str, required=True)
        args = parser.parse_args()

        task = update_task(task_id, args, actor=args["updated_by"])

        return {
            "message": "Task updated successfully",
            "task_id": task.id
        }
    

class TasksByProjectResource(Resource):
    def get(self, project_id):
        tasks = Task.query.filter_by(project_id=project_id).all()

        return [
            {
                "id": t.id,
                "task_id": f"Task-{t.id if t.id >= 1000 else str(t.id).zfill(3)}",
                "title": t.title,
                "description": t.description,
                "status": t.status,
                "priority": t.priority,
                "type": t.type,
                "scope": t.scope,
                "tool": t.tool,
                "due_date": t.due_date.isoformat() + "Z" if t.due_date else None,
                "created_date": t.created_date.isoformat() + "Z" if t.created_date else None,
                "completed_date": t.completed_date.isoformat() + "Z" if t.completed_date else None,
                "last_updated_date": t.last_updated_date.isoformat() + "Z" if t.last_updated_date else None,
                "sprint_id": t.sprint_id,
                "sprint_name": Sprint.query.get(t.sprint_id).name if t.sprint_id else None,
                "project_id": t.project_id,
                "project_name": Project.query.get(t.project_id).name if t.project_id else None,
                "owner_id": t.owner_id,
                "owner_name": f"{User.query.get(t.owner_id).first_name} {User.query.get(t.owner_id).last_name}" if t.owner_id else None,
                "created_by": t.created_by,
                "created_by_name": f"{User.query.filter_by(username=t.created_by).first().first_name} {User.query.filter_by(username=t.created_by).first().last_name}" if t.created_by else None,
            }
            for t in tasks
        ]
    

class TasksBySprintResource(Resource):
    def get(self, sprint_id):
        tasks = Task.query.filter_by(sprint_id=sprint_id).all()

        return [
            {
                "id": t.id,
                "task_id": f"Task-{t.id if t.id >= 1000 else str(t.id).zfill(3)}",
                "title": t.title,
                "description": t.description,
                "status": t.status,
                "priority": t.priority,
                "type": t.type,
                "scope": t.scope,
                "tool": t.tool,
                "due_date": t.due_date.isoformat() + "Z" if t.due_date else None,
                "created_date": t.created_date.isoformat() + "Z" if t.created_date else None,
                "completed_date": t.completed_date.isoformat() + "Z" if t.completed_date else None,
                "last_updated_date": t.last_updated_date.isoformat() + "Z" if t.last_updated_date else None,
                "sprint_id": t.sprint_id,
                "sprint_name": Sprint.query.get(t.sprint_id).name if t.sprint_id else None,
                "project_id": t.project_id,
                "project_name": Project.query.get(t.project_id).name if t.project_id else None,
                "owner_id": t.owner_id,
                "owner_name": f"{User.query.get(t.owner_id).first_name} {User.query.get(t.owner_id).last_name}" if t.owner_id else None,
                "created_by": t.created_by,
                "created_by_name": f"{User.query.filter_by(username=t.created_by).first().first_name} {User.query.filter_by(username=t.created_by).first().last_name}" if t.created_by else None,
            }
            for t in tasks
        ]
    
    
class TasksByUserResource(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first_or_404()
        tasks = Task.query.filter_by(owner_id=user.id).all()

        return [
            {
                "id": t.id,
                "task_id": f"Task-{t.id if t.id >= 1000 else str(t.id).zfill(3)}",
                "title": t.title,
                "description": t.description,
                "status": t.status,
                "priority": t.priority,
                "type": t.type,
                "scope": t.scope,
                "tool": t.tool,
                "due_date": t.due_date.isoformat() + "Z" if t.due_date else None,
                "created_date": t.created_date.isoformat() + "Z" if t.created_date else None,
                "completed_date": t.completed_date.isoformat() + "Z" if t.completed_date else None,
                "last_updated_date": t.last_updated_date.isoformat() + "Z" if t.last_updated_date else None,
                "sprint_id": t.sprint_id,
                "sprint_name": Sprint.query.get(t.sprint_id).name if t.sprint_id else None,
                "project_id": t.project_id,
                "project_name": Project.query.get(t.project_id).name if t.project_id else None,
                "owner_id": t.owner_id,
                "owner_name": f"{User.query.get(t.owner_id).first_name} {User.query.get(t.owner_id).last_name}" if t.owner_id else None,
                "created_by": t.created_by,
                "created_by_name": f"{User.query.filter_by(username=t.created_by).first().first_name} {User.query.filter_by(username=t.created_by).first().last_name}" if t.created_by else None,
            }
            for t in tasks
        ]