from datetime import timedelta

from flask import Flask
from .extensions import db
from .auth.models import User
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["JWT_SECRET_KEY"] = "your-secret-key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    jwt = JWTManager(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .auth.views import auth_blueprint
    from .movies.views import movies_blueprint
    from .recommendations.views import recommendations_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(movies_blueprint)
    app.register_blueprint(recommendations_blueprint)

    return app
