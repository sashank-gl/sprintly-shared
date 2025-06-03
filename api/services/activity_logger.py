from models.activity import Activity
from extensions import db
from datetime import datetime


def log_activity(actor, item_type, item_id, action, field_changed=None, old_value=None, new_value=None, project_id=None, task_id=None):
    activity = Activity(
        actor=actor,
        item_type=item_type,
        item_id=item_id,
        action=action,
        field_changed=field_changed,
        old_value=old_value,
        new_value=new_value,
        project_id=project_id,
        task_id=task_id,
        timestamp=datetime.utcnow()
    )
    
    db.session.add(activity)