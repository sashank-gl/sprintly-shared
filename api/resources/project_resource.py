from flask_restful import Resource, reqparse
from models.project import Project
from models.user import User
from models.activity import Activity
from services.project_service import create_project
from models.sprint import Sprint
from models.task import Task
from extensions import db

class ProjectResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        parser.add_argument("description", required=False)
        parser.add_argument("members", type=list, location='json', required=False)
        parser.add_argument("created_by", type=str, required=True)
        args = parser.parse_args()

        project = create_project(args, actor=args["created_by"], members=args.get("members"))
        return {
            "message": "Project created successfully",
            "project_id": project.id,
            "project_name": project.name
        }, 201
    

    def get(self, project_id=None):
        if project_id is None:
            projects = Project.query.all()
            return [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "created_by": p.created_by,
                    "created_by_name": (
                        f"{User.query.filter_by(username=p.created_by).first().first_name} {User.query.filter_by(username=p.created_by).first().last_name}"
                        if User.query.filter_by(username=p.created_by).first() else None
                    ),
                    "project_manager_id": p.project_manager_id,
                    "project_manager_name": f"{User.query.get(p.project_manager_id).first_name} {User.query.get(p.project_manager_id).last_name}" if User.query.get(p.project_manager_id) else None,
                    "team_name": User.query.filter_by(username=p.created_by).first().team if User.query.filter_by(username=p.created_by).first() else None,
                    "created_date": p.created_date.isoformat() + "Z" if p.created_date else None,
                }
                for p in projects
            ]
        else:
            project = Project.query.get_or_404(project_id)
            project_manager = User.query.get(project.project_manager_id)
            creator = User.query.filter_by(username=project.created_by).first()

            return {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_by": project.created_by,
                "created_by_name": f"{creator.first_name} {creator.last_name}" if creator else None,
                "project_manager_id": project.project_manager_id,
                "project_manager_name": f"{project_manager.first_name} {project_manager.last_name}" if project_manager else None,
                "team_name": creator.team if creator else None,
                "members": [
                    {
                        "id": pm.user.id,
                        "username": pm.username,
                        "first_name": pm.first_name,
                        "last_name": pm.last_name,
                        "team": pm.user.team,
                        "job_title": pm.user.job_title,
                        "role": pm.user.role
                    }
                    for pm in project.project_memberships
                ],
                "sprints": [
                    {
                        "id": sprint.id,
                        "name": sprint.name,
                        "goal": sprint.goal,
                        "status": sprint.status,
                        "start_date": sprint.start_date.isoformat() + "Z" if sprint.start_date else None,
                        "end_date": sprint.end_date.isoformat() + "Z" if sprint.end_date else None,
                        "created_date": sprint.created_date.isoformat() + "Z" if sprint.created_date else None,                        
                        "last_updated_date": sprint.last_updated_date.isoformat() + "Z" if sprint.last_updated_date else None,
                        "planned_release_date": sprint.planned_release_date.isoformat() + "Z" if sprint.planned_release_date else None,                        
                    }
                    for sprint in project.sprints.order_by(Sprint.start_date.asc()).all()
                ],
                "created_date": project.created_date.isoformat() + "Z" if project.created_date else None,

            }
        

    def put(self, project_id):
        from flask_restful import reqparse
        from services.project_service import update_project

        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("description")
        parser.add_argument("project_manager_id", type=int)
        parser.add_argument("members", type=list, location='json', required=False)
        parser.add_argument("updated_by", type=str, required=True)
        args = parser.parse_args()

        project = update_project(project_id, args, actor=args["updated_by"])

        return {
            "message": "Project updated successfully",
            "project_id": project.id
        }
    

class ProjectsByTeamResource(Resource):
    def get(self, team_name):
        team_users = User.query.filter_by(team=team_name).all()
        usernames = [u.username for u in team_users]
        user_ids = [u.id for u in team_users]

        projects = Project.query.filter(
            (Project.created_by.in_(usernames)) | (Project.project_manager_id.in_(user_ids))
        ).all()

        return [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "created_by": p.created_by,
                "created_by_name": (
                    f"{User.query.filter_by(username=p.created_by).first().first_name} {User.query.filter_by(username=p.created_by).first().last_name}"
                    if User.query.filter_by(username=p.created_by).first() else None
                ),
                "project_manager_id": p.project_manager_id,
                "project_manager_name": f"{User.query.get(p.project_manager_id).first_name} {User.query.get(p.project_manager_id).last_name}" if User.query.get(p.project_manager_id) else None,
                "team_name": User.query.filter_by(username=p.created_by).first().team if User.query.filter_by(username=p.created_by).first() else None,
                "created_date": p.created_date.isoformat() + "Z" if p.created_date else None
            }
            for p in projects
        ]
    

class ProjectsByUserResource(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first_or_404()
        
        member_projects = set(pm.project for pm in user.project_memberships)
        created_projects = set(Project.query.filter_by(created_by=user.username).all())
        managed_projects = set(Project.query.filter_by(project_manager_id=user.id).all())

        all_projects = list(member_projects.union(created_projects, managed_projects))

        return [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "created_by": p.created_by,
                "created_by_name": (
                    f"{User.query.filter_by(username=p.created_by).first().first_name} {User.query.filter_by(username=p.created_by).first().last_name}"
                    if User.query.filter_by(username=p.created_by).first() else None
                ),
                "project_manager_id": p.project_manager_id,
                "project_manager_name": f"{User.query.get(p.project_manager_id).first_name} {User.query.get(p.project_manager_id).last_name}" if User.query.get(p.project_manager_id) else None,
                "team_name": User.query.filter_by(username=p.created_by).first().team if User.query.filter_by(username=p.created_by).first() else None,
                "created_date": p.created_date.isoformat() + "Z" if p.created_date else None,
                "last_user_activity": (
                    Activity.query
                    .filter_by(project_id=p.id, actor=username)
                    .order_by(Activity.timestamp.desc())
                    .first()
                    .timestamp.isoformat() + "Z"
                    if Activity.query.filter_by(project_id=p.id, actor=username).first()
                    else None
                )
            }
            for p in all_projects
        ]


class ProjectOverviewResource(Resource):
    def get(self, project_id):
        project = Project.query.get_or_404(project_id)

        tasks = Task.query.filter_by(project_id=project_id).all()

        status_counts = {"To Do": 0, "In Progress": 0, "Completed": 0, "On Hold": 0}
        priority_counts = {"Critical":0, "High": 0, "Medium": 0, "Low": 0}

        for task in tasks:
            if task.status in status_counts:
                status_counts[task.status] += 1
            else:
                status_counts[task.status] = 1

            if task.priority in priority_counts:
                priority_counts[task.priority] += 1
            else:
                priority_counts[task.priority] = 1

        sprints = Sprint.query.filter_by(project_id=project_id).all()

        return {
            "project_id": project.id,
            "project_name": project.name,
            "total_tasks": len(tasks),
            "task_status_counts": status_counts,
            "task_priority_counts": priority_counts,
            "total_sprints": len(sprints)
        }
    

class AddProjectMemberResource(Resource):
    def post(self, project_id):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("email", required=True)
        parser.add_argument("first_name", required=True)
        parser.add_argument("last_name", required=True)
        parser.add_argument("team", required=True)
        parser.add_argument("job_title", required=True)
        parser.add_argument("role", required=True)
        args = parser.parse_args()

        project = Project.query.get_or_404(project_id)

        user = User.query.filter_by(username=args["username"]).first()
        if not user:
            user = User(
                username=args["username"],
                email=args["email"],
                first_name=args["first_name"],
                last_name=args["last_name"],
                team=args["team"],
                job_title=args["job_title"],
                role=args["role"]
            )
            db.session.add(user)
            db.session.flush() 

        from models.user import ProjectMember

        existing_pm = ProjectMember.query.filter_by(user_id=user.id, project_id=project.id).first()
        if existing_pm:
            return {"message": "User is already a member of the project"}, 400

        pm = ProjectMember(
            user_id=user.id,
            project_id=project.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            project_name=project.name,
            project_manager_name=f"{User.query.get(project.project_manager_id).first_name} {User.query.get(project.project_manager_id).last_name}" if project.project_manager_id else None
        )
        db.session.add(pm)
        db.session.commit()

        return {"message": f"User {user.username} added to project {project.id}"}, 200