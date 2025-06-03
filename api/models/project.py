from extensions import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(80), db.ForeignKey('users.username'))
    project_manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sprints = db.relationship('Sprint', backref='project', lazy='dynamic')
    tasks = db.relationship('Task', backref='project', lazy='dynamic')
    activities = db.relationship('Activity', backref='project', lazy='dynamic')

    def __repr__(self):
        return f"<Project {self.name}>"
