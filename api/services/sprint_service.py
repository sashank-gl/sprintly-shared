from models.sprint import Sprint
from app import db
from services.activity_logger import log_activity
from datetime import datetime

def parse_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d")
    return None

def create_sprint(data, actor):
    sprint = Sprint(
        name=data.get("name"),
        goal=data.get("goal"),
        status=data.get("status", "Planning"),
        start_date=parse_date(data.get("start_date")),
        end_date=parse_date(data.get("end_date")),
        created_date=datetime.utcnow(),
        planned_release_date=parse_date(data.get("planned_release_date")),
        project_id=data.get("project_id"),
        created_by=actor
    )

    db.session.add(sprint)
    db.session.flush() 

    log_activity(
        actor=actor,
        item_type="Sprint",
        item_id=sprint.id,
        action="created",
        project_id=sprint.project_id
    )

    db.session.commit()
    return sprint

def update_sprint(sprint_id, data, actor):
    sprint = Sprint.query.get_or_404(sprint_id)

    fields_to_check = [
        "name", "goal", "status", "start_date", "end_date",
        "planned_release_date", "project_id"
    ]

    for field in fields_to_check:
        new_value = data.get(field)
        old_value = getattr(sprint, field)

        if field in ["start_date", "end_date", "planned_release_date"]:
            new_value = parse_date(new_value) if new_value else None

        if new_value is not None and str(new_value) != str(old_value):
            log_activity(
                actor=actor,
                item_type="Sprint",
                item_id=sprint.id,
                action="updated",
                field_changed=field,
                old_value=str(old_value),
                new_value=str(new_value),
                project_id=sprint.project_id
            )
            setattr(sprint, field, new_value)

    sprint.last_updated_date = datetime.utcnow()

    db.session.commit()
    return sprint