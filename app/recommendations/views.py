from flask import Blueprint

recommendations_blueprint = Blueprint("recommendations", __name__)


@recommendations_blueprint.route("/login")
def login():
    return "Login Page"
