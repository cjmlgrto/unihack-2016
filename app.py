from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

global_users = {}

global_users = {}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/user_database2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	full_name = db.Column(db.String)
	calendar = db.Column(db.String)
	groups = db.relationship('Group', backref='user', lazy='dynamic')

	def __init__(self, name, calendar=None, full_name=None):
		self.name = name
		self.full_name = full_name
		self.calendar = calendar

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	group_code = db.Column(db.String, unique=False)
	person_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, group_code, person_id):
		self.group_code = group_code
		self.person_id = person_id

def generate_code():
	key = str(hash(str(datetime.now())))
	key = key[0:6]
	return str(key)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def check_username():
	username_exists = False
	username = request.form['username']
	db_user = User.query.filter_by(name=username).first()
	if db_user is not None:
		username_exists = True
		url = '/user/' + username
		return redirect(url)
	else:
		username_exists = False
		return render_template('index.html', username_exists=username_exists)

@app.route('/new_user/')
def new_user():
	username = generate_code()
	global_users[username] = []
	user = User(username)
	db.session.add(user)
	db.session.commit()
	global_users[username] = []

	url = '/user/' + username
	return redirect(url)

@app.route('/user/<username>')
def user(username):
	db_user = User.query.filter_by(name=username).first()

	events = global_users[username]

	return render_template('user.html', user=db_user, events=events)

@app.route('/user/<username>/create_event/<start>/<end>')
def create_event(username, start, end):
	event = [start, end]
<<<<<<< HEAD:app.py
	global_users[username].append(event)
	url = '/user/' + username
	return redirect(url)
=======

	global_users[username].append(event)

	url = '/user/' + username
	return redirect(url)

	
>>>>>>> 18b5dfc53269c91c2feaf5ca0c6ce2a085f9dd99:prototype/app.py

@app.route('/new_group/<username>')
def new_group(username):
	group_code = generate_code()
	person_id = User.query.filter_by(name=username).first().id
	group = Group(group_code, person_id)
	db.session.add(group)
	db.session.commit()
	url = '/group/' + group_code
	return redirect(url)

@app.route('/group/<group_code>')
def group(group_code):
	users = Group.query.filter_by(group_code=group_code).all()
	group_code = group_code
	return render_template('group.html', users=users, group_code=group_code)

@app.route('/group/<group_code>/add_users', methods=['POST'])
def add_user(group_code):
	username = request.form['username']
	person_id = User.query.filter_by(name=username).first().id
	new_user = Group(group_code, person_id)
	db.session.add(new_user)
	db.session.commit()
	url = '/group/' + group_code
	return redirect(url)

<<<<<<< HEAD:app.py
=======
def add_user(group_code):
    username = request.form['username']
    person = User.query.filter_by(name=username).first()
    url = '/group/' + group_code
    if person is None:
        return redirect(url)
    else:
        person_id = person.id
        group = Group.query.filter_by(group_code=group_code).first()
        for user in group.users:
            if user.id == person_id:
                return redirect(url)
        user = Group(group_code, person_id)
        db.session.add(user)
        db.session.commit()
        return redirect(url)
        

# users = Group.query.filter_by(group_code=group_code).first()
# 	user_ids = [i.User.id for i in users]
# 	userid = User.query.filter_by(name=username).first()
# 	url = '/group/' + group_code
# 	if userid == None:
# 		return redirect(url)
# 	else:
# 		if userid in user_ids:
# 			return redirect(url)
# 		else:
# 			user = Group(group_code, userid)
# 			db.session.add(user)
# 			db.session.commit()
# 			return redirect(url)


>>>>>>> 18b5dfc53269c91c2feaf5ca0c6ce2a085f9dd99:prototype/app.py
if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)