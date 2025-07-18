from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ... rest of your configuration ...
jwt = JWTManager(app)
mail = Mail(app)
photos = UploadSet('photos', IMAGES)
videos = UploadSet('videos', VIDEO)

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.utils.config.Config')
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    configure_uploads(app, photos)
    configure_uploads(app, videos)
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.incident_routes import incident_bp
    from app.routes.admin_routes import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(incident_bp, url_prefix='/api/incidents')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    return app