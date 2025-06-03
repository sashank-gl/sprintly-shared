from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import text
import logging
from extensions import db

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"],}})
    api = Api(app)
    app.config.from_object('config.DevConfig')
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from models import project, task, sprint, user, activity
        db.create_all()

    from routes import project_blueprint, task_blueprint, sprint_blueprint, activity_blueprint, user_blueprint

    app.register_blueprint(project_blueprint)
    app.register_blueprint(task_blueprint)
    app.register_blueprint(sprint_blueprint)
    app.register_blueprint(activity_blueprint)
    app.register_blueprint(user_blueprint)
   
    @app.route("/")
    def home():
        return "Sprintly is live and connected to the database!"
    return app

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)