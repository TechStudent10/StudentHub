from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient

classViews = Blueprint("ClassViews", __name__)
client = MongoClient()

db = client.StudentHub

users = db.users
classes = db.classes

@classViews.route("/<class_id>")
def viewClass(class_id):
	if 'current_user' in session:
		return render_template("class.html", user=session['current_user'])
	return "You need to login!"

@classViews.route("/create")
def create():
	if 'current_user' in session:
		return render_template("createClass.html")
	return "You need to login!"

@classViews.route("/join")
def join():
	if 'current_user' in session:
		return render_template("joinClass.html", username=session['current_user']['username'])
	return "You need to login!"