from flask import Flask, render_template, session, request, flash
from api import api
from userViews import userViews
from classViews import classViews
from costumEncoder import MyEncoder

import os, string, random

app = Flask(__name__, template_folder=os.path.join('website', 'templates'), static_folder=os.path.join('website', 'static'))
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(userViews)
app.register_blueprint(classViews, url_prefix="/class")

app.secret_key = "StudentHub"
app.json_encoder = MyEncoder

@app.route("/")
def main():
	return render_template("index.html")

@app.route("/logout")
def logout():
	if 'current_user' in session:
		session.pop('current_user')
		return "Logged out."
	return "You haven't even logged in!"

if __name__ == '__main__':
	app.run(debug=True, port=7000)