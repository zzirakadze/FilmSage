from flask import Blueprint

movies_blueprint = Blueprint("movies", __name__)


@movies_blueprint.route("/login")
def login():
    return "Login Page"
