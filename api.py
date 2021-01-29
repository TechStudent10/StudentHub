from flask import Blueprint, request, session
from pymongo import MongoClient
import random, string

api = Blueprint("API", __name__)
client = MongoClient()

db = client.StudentHub

users = db.users
classes = db.classes

def generateRandomKey(length=6):
	key = ''.join(random.choices(string.ascii_uppercase, k=length))
	return key

@api.route("/", methods=['POST', 'GET'])
def mainAPI():
	if request.method == 'GET':
		return "You are not allowed to visit this Endpoint."
	return db

@api.route("/signup", methods=['POST'])
def signup():
	form = request.form

	username = form.get('username')
	password = form.get('password')

	user = {
		'username': username,
		'password': password,
		'classes': []
	}

	users.insert_one(user)
	return user

@api.route("/login", methods=['POST'])
def login():
	form = request.form

	username = form.get('username')
	password = form.get('password')

	user = users.find_one({"username": username, "password": password})
	if user:
		session['current_user'] = user
		return user
	return "", 404

@api.route("/createClass", methods=['POST'])
def createClass():
	form = request.form

	name = form.get('name')
	room = form.get('room')
	teacher = form.get('username')
	code = generateRandomKey()

	classInfo = {
		'name': name,
		'room': room,
		'code': code,
		'students': []
	}

	classes.insert_one(classInfo)
	return classInfo

@api.route("/joinClass", methods=['POST'])
def joinClass():
	form = request.form

	username = form.get('username')
	classCode = form.get('classCode')

	classInfo = classes.find_one({"code": classCode})
	if classInfo:
		user_joining = users.find_one({"username": username})
		if user_joining:
			userData = {}
			for i in user_joining:
				if i == "password":
					pass
				elif i == "classes":
					pass
				else:
					userData[i] = user_joining[i]

			print(user_joining)

			classInfo['students'].append(userData)
			user_joining['classes'].append(classInfo)

		return classInfo
	return "", 404