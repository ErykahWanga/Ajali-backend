from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from flask_uploads import UploadSet, IMAGES, configure_uploads, VIDEO
from app.utils.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
photos = UploadSet('photos', IMAGES)
videos = UploadSet('videos', VIDEO)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    configure_uploads(app, photos)
    configure_uploads(app, videos)
    
    # Register blueprints here if needed
    # from app.routes.auth_routes import auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    return app

# This line is typically not included in the application code.
# It's a command for the terminal to set the environment variable.
# set FLASK_APP=app:create_app
# flask db init