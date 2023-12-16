from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_smorest import Blueprint
from marshmallow import ValidationError

from .models import Auth
from .schema import UserRegistrationSchema, UserLoginSchema

auth_blp = Blueprint(
    "auth-controller",
    "auth",
    url_prefix="/auth",
    description="Authentication operations",
)

user_registration_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()


@auth_blp.route("/register")
class Register(MethodView):
    @auth_blp.arguments(user_registration_schema)
    @auth_blp.response(201, user_registration_schema)
    def post(self, user_data):
        try:
            data = user_registration_schema.load(user_data)
        except ValidationError as err:
            return jsonify({"message": err.messages, "status_code": 400}), 400
        username = data.get("username")
        email = data.get("email")
        if Auth.user_exists(username):
            return (
                jsonify(
                    {
                        "message": f"User: '{username}' already exists",
                        "status_code": 403,
                    }
                ),
                403,
            )
        if Auth.email_exists(email):
            return jsonify({"message": f"Email: '{email}' already exists"}), 403
        Auth.add_user(**data)
        return (
            jsonify({"message": "User registered successfully", "status_code": 201}),
            201,
        )


@auth_blp.route("/login")
class Login(MethodView):
    @auth_blp.arguments(user_login_schema)
    @auth_blp.response(200, user_login_schema)
    def post(self, user_data):
        try:
            data = user_login_schema.load(user_data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        user = Auth.check_user(data["username"], data["password"])
        if user:
            access_token, refresh_token = Auth.create_tokens(user.id)
            return jsonify(access_token=access_token, refresh_token=refresh_token), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401


@auth_blp.route("/refresh")
class Refresh(MethodView):
    @staticmethod
    @auth_blp.doc(security=[{"jwt": []}])
    @jwt_required(refresh=True)
    def post():
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return jsonify(access_token=new_access_token), 200


#  """This is an example of protected route"""
# @auth_blp.route("/protected", methods=["GET"])
# @auth_blp.doc(security=[{"jwt": []}])
# @jwt_required()
# def protected():
#     current_user_id = get_jwt_identity()
#     return jsonify(logged_in_as=Auth.get_user(current_user_id)), 200
