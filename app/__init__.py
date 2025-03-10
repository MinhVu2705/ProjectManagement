from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_apscheduler import APScheduler
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from .utils import get_user_from_cookie

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()
scheduler = APScheduler()
api = Api()
jwt = JWTManager()
cache = Cache()

class Config:
    SECRET_KEY = 'your_secret_key'
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # Dùng cho JWT
    CACHE_TYPE = 'simple'  # Cấu hình caching đơn giản

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    api.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    # Import routes, models, and API routes
    with app.app_context():
        from . import routes, models
        db.create_all()

    @app.context_processor
    def inject_user():
        return dict(get_user_from_cookie=get_user_from_cookie)

    return app
