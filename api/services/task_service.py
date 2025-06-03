from models.task import Task
from app import db
from services.activity_logger import log_activity
from datetime import datetime


def parse_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d")
    return None


def create_task(data, actor):
    description = data.get("description")
    if isinstance(description, str):
        description = [description]
    elif description is None:
        description = []
    task = Task(
        title=data.get("title"),
        description=description,
        status=data.get("status"),
        priority=data.get("priority"),
        type=data.get("type"),
        scope=data.get("scope"),
        tool=data.get("tool"),
        due_date=parse_date(data.get("due_date")),
        created_date=datetime.utcnow(),
        project_id=data.get("project_id"),
        sprint_id=data.get("sprint_id"),
        owner_id=data.get("owner_id"),
        created_by=actor,
        last_updated_date=datetime.utcnow()
    )

    db.session.add(task)
    db.session.flush()  

    log_activity(
        actor=actor,
        item_type="Task",
        item_id=task.id,
        action="created",
        project_id=task.project_id,
        task_id=task.id
    )

    db.session.commit()
    return task


def update_task(task_id, data, actor):
    task = Task.query.get_or_404(task_id)
    previous_status = task.status

    fields_to_check = [
        "title", "description", "status", "priority", "type",
        "scope", "tool", "due_date", "sprint_id", "owner_id"
    ]

    for field in fields_to_check:
        new_value = data.get(field)
        if field == "description":
            if isinstance(new_value, str):
                new_value = [new_value]
            elif new_value is None:
                new_value = []
            old_value = getattr(task, field) or []
            max_len = max(len(old_value), len(new_value))
            for i in range(max_len):
                old_line = old_value[i] if i < len(old_value) else None
                new_line = new_value[i] if i < len(new_value) else None
                if old_line != new_line:
                    log_activity(
                        actor=actor,
                        item_type="Task",
                        item_id=task.id,
                        action="updated",
                        field_changed=f"description[{i}]",
                        old_value=old_line,
                        new_value=new_line,
                        project_id=task.project_id,
                        task_id=task.id
                    )
            setattr(task, field, new_value)
        else:
            old_value = getattr(task, field)
            if new_value is not None and str(new_value) != str(old_value):
                log_activity(
                    actor=actor,
                    item_type="Task",
                    item_id=task.id,
                    action="updated",
                    field_changed=field,
                    old_value=str(old_value),
                    new_value=str(new_value),
                    project_id=task.project_id,
                    task_id=task.id
                )
                setattr(task, field, new_value) 

    new_status = task.status
    if previous_status != "Completed" and new_status == "Completed":
        task.completed_date = datetime.utcnow()
    elif previous_status == "Completed" and new_status != "Completed":
        task.completed_date = None

    if "due_date" in data and data.get("due_date") is not None:
        task.due_date = parse_date(data.get("due_date"))

    task.last_updated_date = datetime.utcnow()  

    db.session.commit()  
    return task  