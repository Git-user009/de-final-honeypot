from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a strong secret key
    app.config['DEBUG'] = True  # Enable debug mode during development

    # Enable CORS
    CORS(app, supports_credentials=True)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # Import and register the Blueprint
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # Create database tables
        db.create_all()

    return app