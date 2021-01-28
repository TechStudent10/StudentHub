from flask import Blueprint, request, session
from flask_sqlalchemy import SQLAlchemy

api = Blueprint("API", __name__)

@api.route("/")
def mainAPI():
	return "You are not allowed to visit this Endpoint."