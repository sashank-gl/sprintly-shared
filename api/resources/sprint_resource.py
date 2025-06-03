from flask_restful import Resource, reqparse
from services.sprint_service import create_sprint
from extensions import db

class SprintResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        parser.add_argument("goal", required=False)
        parser.add_argument("status", required=False)
        parser.add_argument("start_date", required=False) 
        parser.add_argument("end_date", required=False)
        parser.add_argument("planned_release_date", required=False)
        parser.add_argument("project_id", type=int, required=True)
        parser.add_argument("created_by", type=str, required=True)
        args = parser.parse_args()

        sprint = create_sprint(args, actor=args["created_by"])
        return {
            "message": "Sprint created successfully",
            "sprint_id": sprint.id,
            "sprint_name": sprint.name,
            "project_id": sprint.project_id
        }, 201
    

    def get(self, sprint_id):
        from models.sprint import Sprint
        sprint = Sprint.query.get_or_404(sprint_id)
        return {
            "id": sprint.id,
            "name": sprint.name,
            "goal": sprint.goal,
            "status": sprint.status,
            "start_date": sprint.start_date.isoformat() + "Z" if sprint.start_date else None,
            "end_date": sprint.end_date.isoformat() + "Z" if sprint.end_date else None,
            "created_date": sprint.created_date.isoformat() + "Z" if sprint.created_date else None,
            "last_updated_date": sprint.last_updated_date.isoformat() + "Z" if sprint.last_updated_date else None,
            "planned_release_date": sprint.planned_release_date.isoformat() + "Z" if sprint.planned_release_date else None,
            "project_id": sprint.project_id,
            "created_by": sprint.created_by
        }
    

    def put(self, sprint_id):
        from flask_restful import reqparse
        from services.sprint_service import update_sprint

        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("goal")
        parser.add_argument("status")
        parser.add_argument("start_date")
        parser.add_argument("end_date")
        parser.add_argument("planned_release_date")
        parser.add_argument("project_id", type=int)
        parser.add_argument("updated_by", type=str, required=True)
        args = parser.parse_args()

        sprint = update_sprint(sprint_id, args, actor=args["updated_by"])

        return {
            "message": "Sprint updated successfully",
            "sprint_id": sprint.id
        }