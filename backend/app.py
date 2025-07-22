# /backend/app.py
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig
from models import db, bcrypt
from routes.auth_routes import auth_bp
from routes.incident_routes import incident_bp
from routes.admin_routes import admin_bp

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(incident_bp, url_prefix='/incidents')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

app = create_app()

if __name__ == '__main__':
    app.run()