from flask import Blueprint, render_template, session, request, redirect, url_for

userViews = Blueprint("UserViews", __name__)

@userViews.route("/signup")
def signup():
	return render_template("signup.html")

@userViews.route("/login")
def login():
	return render_template("login.html")