from extensions import db

class ProjectMember(db.Model):
    __tablename__ = 'project_members'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    username = db.Column(db.String(80))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    project_name = db.Column(db.String(120))
    project_manager_name = db.Column(db.String(100))
    user = db.relationship('User', backref=db.backref('project_memberships', cascade='all, delete-orphan'))
    project = db.relationship('Project', backref=db.backref('project_memberships', cascade='all, delete-orphan'))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    team = db.Column(db.String(50))
    job_title = db.Column(db.String(120))
    role = db.Column(db.String(50))
    avatar_url = db.Column(db.String(255), nullable=True)

    tasks_assigned = db.relationship('Task', backref='owner', foreign_keys='Task.owner_id')
    tasks_created = db.relationship('Task', backref='creator', foreign_keys='Task.created_by')
    projects_created = db.relationship('Project', backref='creator', foreign_keys='Project.created_by')
    managed_projects = db.relationship('Project', backref='project_manager', foreign_keys='Project.project_manager_id')
    sprints_created = db.relationship('Sprint', backref='creator', foreign_keys='Sprint.created_by')
    activities = db.relationship('Activity', backref='actor_username', foreign_keys='Activity.actor')
    
    def __repr__(self):
        return f"<User {self.username}>"