from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint
from .schema import GetUsersSchema
from .utils import UserActions

users_blp = Blueprint(
    "users-controller",
    "users",
    url_prefix="/users",
    description="User related operations",
)

user_actions = UserActions()


@users_blp.route("/me")
class Me(MethodView):
    @users_blp.doc(security=[{"jwt": []}])
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        return jsonify({"user_id": user_id}), 200


@users_blp.route("/user/<string:email>")
class User(MethodView):
    @jwt_required()
    @users_blp.doc(security=[{"jwt": []}])
    def get(self, email):
        if GetUsersSchema().validate({"email": email}):
            return jsonify({"message": "Invalid email"}), 400
        if user_actions.get_user_by_email(email):
            return jsonify(user_actions.get_user_by_email(email)), 200
        return jsonify({"message": "User not found"}), 404

    @jwt_required()
    @users_blp.doc(security=[{"jwt": []}])
    def post(self):
        """
        updates username and surname
        :return: updated user
        :rtype: json
        """
