from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_jwt_extended import create_access_token, create_refresh_token


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Auth:
    password_pattern = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$"
    )
    email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    @staticmethod
    def hash_password(password: str) -> str:
        return generate_password_hash(password)

    @staticmethod
    def check_password(password_hash: str, password: str) -> bool:
        return check_password_hash(password_hash, password)

    @staticmethod
    def validate_password_format(password: str) -> bool:
        return bool(Auth.password_pattern.match(password))

    @staticmethod
    def validate_email_format(email: str) -> bool:
        return bool(Auth.email_pattern.match(email))

    @staticmethod
    def add_user(
        name: str,
        surname: str,
        email: str,
        username: str,
        password: str,
    ) -> None:
        try:
            password_hash = Auth.hash_password(password)
            new_user = User(
                name=name,
                surname=surname,
                email=email,
                username=username,
                password=password_hash,
            )
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print("Error adding user to database: ", e)

    @staticmethod
    def check_user(username: str, password: str):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return user
        return None

    @staticmethod
    def user_exists(username: str) -> bool:
        try:
            return User.query.filter_by(username=username).first() is not None
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def email_exists(email: str) -> bool:
        try:
            return User.query.filter_by(email=email).first() is not None
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def create_tokens(user_id):
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        return access_token, refresh_token

    @staticmethod
    def get_user(user_id: User.id) -> str | None:
        try:
            user = User.query.get(user_id)
            return f"{user.name} {user.surname}"
        except Exception as e:
            print(e)
            return None
