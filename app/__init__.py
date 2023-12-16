from datetime import timedelta

from flask import Flask
from flask_smorest import Api

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

    # swagger
    app.config["API_TITLE"] = "FilmSage API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_JSON_PATH"] = "openapi.json"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)
    api.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )

    JWTManager(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .auth.views import auth_blp
    from .users.views import users_blp
    from .movies.views import movies_blueprint
    from .recommendations.views import recommendations_blueprint

    api.register_blueprint(auth_blp)
    api.register_blueprint(users_blp)
    app.register_blueprint(movies_blueprint)
    app.register_blueprint(recommendations_blueprint)

    return app
