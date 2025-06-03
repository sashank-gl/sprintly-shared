from extensions import db
from datetime import datetime 

class Sprint(db.Model):
    __tablename__ = 'sprints'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    goal = db.Column(db.Text) 
    status = db.Column(db.String(50), default='Planning') 
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    planned_release_date = db.Column(db.DateTime, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    created_by = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False) 
    tasks = db.relationship('Task', backref='sprint', lazy='dynamic')

    def __repr__(self):
        return f"<Sprint {self.name}>"
