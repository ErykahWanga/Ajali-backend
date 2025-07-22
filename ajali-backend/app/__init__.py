# /app/__init__.py

from flask import Flask
from flask_cors import CORS
from .utils.config import DevelopmentConfig
from .utils.database import db, bcrypt, jwt, migrate

def create_app(config_class=DevelopmentConfig):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Import and register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.incident_routes import incident_bp
    from .routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(incident_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # This is needed for Flask-Migrate to find the models
    from . import models

    return app