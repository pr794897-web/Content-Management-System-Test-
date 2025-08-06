from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize the extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Ensure you have the 'main.login' route defined

def create_app():
    # Create Flask app instance
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration from instance/config.py
    try:
        app.config.from_pyfile('config.py', silent=False)  # Set silent=False to catch missing config
    except FileNotFoundError:
        raise Exception("config.py is missing, please create it!")

    # Check if upload folder exists, and create it if necessary
    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])  # Create the folder if it doesn't exist

    # Initialize the extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import User model for login manager
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # This function loads the user by ID for login sessions
        return User.query.get(int(user_id))

    # Register blueprints (routes)
    from .routes import main  # Make sure you have routes.py where 'main' is defined
    app.register_blueprint(main)

    return app
