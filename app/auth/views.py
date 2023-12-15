from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from .models import Auth
from .schema import UserRegistrationSchema, UserLoginSchema
from marshmallow import ValidationError

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

user_registration_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()


@auth_blueprint.route("/register", methods=["POST"])
def register():
    try:
        data = user_registration_schema.load(request.json)
    except ValidationError as err:
        print("ERROR", err.messages)
        return jsonify({"message": err.messages, "status_code": 400}), 400
    username = data.get("username")
    email = data.get("email")
    if Auth.user_exists(username):
        return jsonify({"message": f"User: '{username}' already exists",
                        "status_code": 403}), 403
    if Auth.email_exists(email):
        return jsonify({"message": f"Email: '{email}' already exists"}), 403
    Auth.add_user(**data)
    return jsonify({"message": "User registered successfully", "status_code": 201}), 201


@auth_blueprint.route("/login", methods=["POST"])
def login():
    try:
        data = user_login_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user = Auth.check_user(data["username"], data["password"])
    if user:
        access_token, refresh_token = Auth.create_tokens(user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200


@auth_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=Auth.get_user(current_user_id)), 200
