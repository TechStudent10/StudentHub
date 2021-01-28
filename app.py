from flask import Flask, render_template, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from api import api

import os, string, random

app = Flask(__name__, template_folder=os.path.join('website', 'templates'), static_folder=os.path.join('website', 'static'))
app.register_blueprint(api, url_prefix="/api")

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "StudentHub"

db = SQLAlchemy(app)

class User(db.Model):
	_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(50), nullable=False, unique=True)

	def __init__(self, name, password):
		self.name = name
		self.password = password

class Rooms(db.Model):
	_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	posts = db.relationship("Posts")

	def __init__(self, name, posts):
		self.name = name
		self.posts = map(Post, posts)

class Post(db.Model):
	_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	poster = db.relationship("User")
	comments = db.relationship("Comment")

	def __init__(self, name, poster, comments):
		self.name = name
		self.poster = map(User, poster)
		self.comments = map(Comment, comments)

class Comment(db.Model):
	_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	poster = db.relationship("User")

	def __init__(self, name, poster):
		self.name = name
		self.poster = map(User, poster)

@app.route("/")
def main():
	return render_template("index.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		form = request.form

		username = form.get('username')
		password = form.get('password')

		user = User(username, password)
		db.session.add(user)
		db.session.commit()

		return "Signed Up!"
	else:
		return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		form = request.form

		username = form.get('username')
		password = form.get('password')

		user = User.query.filter_by(name=username, password=password).first()
		try:
			userInfo = {
				'username': user.name,
				'password': user.password
			}

			session['currentUser'] = userInfo

			return "Logged In!"
		except AttributeError:
			return "User not found.", 404
	else:
		return render_template("login.html")

if __name__ == '__main__':
	app.run(debug=True, port=7000)