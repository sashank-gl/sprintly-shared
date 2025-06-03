from models.project import Project
from extensions import db
from services.activity_logger import log_activity
from datetime import date

def create_project(data, actor, members=None):

    from models.user import User

    creator = User.query.filter_by(username=actor).first_or_404()
    manager = User.query.filter_by(team=creator.team, job_title="Manager").first()
    if not manager:
        manager = creator

    existing_project = Project.query.join(User, Project.created_by == User.username).filter(
        Project.name == data.get("name"),
        User.team == creator.team
    ).first()

    if existing_project:
        raise ValueError(f"A project named '{data.get('name')}' already exists in the team '{creator.team}'.")

    project = Project(
        name=data.get("name"),
        description=data.get("description"),
        created_by=creator.username,
        project_manager_id=manager.id
    )

    db.session.add(project)
    db.session.flush()

    member_usernames = members if members is not None else []
    if not member_usernames:
        member_usernames = [creator.username]
    
    from models.user import User, ProjectMember
    selected_members = User.query.filter(User.username.in_(member_usernames)).all()
    
    for member in selected_members:
        pm = ProjectMember(
            user_id=member.id,
            project_id=project.id,
            username=member.username,
            first_name=member.first_name,
            last_name=member.last_name,
            project_name=project.name,
            project_manager_name=f"{manager.first_name} {manager.last_name}" if manager else None
        )
        db.session.add(pm)

    log_activity(
        actor=actor,
        item_type="Project",
        item_id=project.id,
        action="created",
        project_id=project.id
    )

    db.session.commit()
    return project


def update_project(project_id, data, actor):
    project = Project.query.get_or_404(project_id)
    fields_to_check = ["name", "description", "project_manager_id"]

    for field in fields_to_check:
        new_value = data.get(field)
        old_value = getattr(project, field)

        if new_value is not None and str(new_value) != str(old_value):
            log_activity(
                actor=actor,
                item_type="Project",
                item_id=project.id,
                action="updated",
                field_changed=field,
                old_value=str(old_value),
                new_value=str(new_value),
                project_id=project.id
            )
            setattr(project, field, new_value)

    member_usernames = data.get("members")
    if member_usernames is not None:
        from models.user import User, ProjectMember
        selected_members = User.query.filter(User.username.in_(member_usernames)).all()
        # Remove existing members
        ProjectMember.query.filter_by(project_id=project.id).delete()
        # Add new members
        manager = User.query.filter_by(id=project.project_manager_id).first()
        for member in selected_members:
            pm = ProjectMember(
                user_id=member.id,
                project_id=project.id,
                username=member.username,
                first_name=member.first_name,
                last_name=member.last_name,
                project_name=project.name,
                project_manager_name=f"{manager.first_name} {manager.last_name}" if manager else None
            )
            db.session.add(pm)

    db.session.commit()
    return project