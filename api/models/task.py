from extensions import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.JSON)
    status = db.Column(db.String(50)) 
    priority = db.Column(db.String(50)) 
    type = db.Column(db.String(50))  
    scope = db.Column(db.String(50)) 
    tool = db.Column(db.String(100)) 
    due_date = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    completed_date = db.Column(db.DateTime)
    last_updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sprint_id = db.Column(db.Integer, db.ForeignKey('sprints.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.Column(db.String(80), db.ForeignKey('users.username'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    activities = db.relationship('Activity', backref='task', foreign_keys='Activity.task_id')
    
    def __repr__(self):
        return f"<Task {self.title}>"