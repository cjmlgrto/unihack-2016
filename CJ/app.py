from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from base64 import b64encode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test4.db'
db = SQLAlchemy(app)


################ DATABASE SETUP ########################
# catz

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    calendar = db.Column(db.String)
    groups = db.relationship('Group', backref='user', lazy='dynamic')

    def __init__(self, name, calendar = ""):
        self.name = name
        self.calendar = calendar

    #def __repr__(self):
    #	return self.name

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	groupCode = db.Column(db.Integer, unique=False)
	person_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, groupCode, person_id):
		self.groupCode = groupCode
		self.person_id = person_id


################## ROUTING ########################

def returnNames(arr):
	return []

# displays the home page
@app.route('/')
def home():
	return render_template('home.html')

# checks for username availability
@app.route('/', methods=['POST'])
def check_username():
	username = request.form['username']
	dbUsername = User.query.filter_by(name=username).all()
	if dbUsername != []:
		return render_template('home.html', username_exists=True, username=username)
	else:
		return render_template('home.html', username_exists=False, username=username)

# renders a user's page
@app.route('/user/<username>')
def user(username):
	dbUsername = User.query.filter_by(name=username).all()
	# Creates a list of the users with that name
	if dbUsername != []:
		#events = faux_users[username]
		events = dbUsername[0].calendar
		# What is the code above?
		#return render_template('user.html', username=username, events=events)
		return render_template('user.html', username=username)
	else:
		return render_template('404.html', value=username)

# creates a new user's page
@app.route('/new_user/<username>')
def new_user(username):
	dbUsername = User.query.filter_by(name=username).all()
	if dbUsername == []:
		me = User(username)
		db.session.add(me)
		db.session.commit()
		url = '/user/' + username
		return redirect(url)
	return render_template('404.html', value=username)


###################	EDITS BY ALEX UP TO HERE ##############

# creates a new group
@app.route('/new_group/')
def new_group():
	group_code = generate_code()
	faux_groups[group_code] = []
	url = '/group/' + group_code
	return redirect(url)

# generates a code
def generate_code():
	key = b64encode(str(hash(datetime.now())))
	return key

# renders a group page
@app.route('/group/<group_code>')
def group(group_code):
	if group_code in faux_groups:
		return render_template('group.html', group_code=group_code, users=users, username=usernames)
	else:
		return render_template('404.html', value=group_code)

# creates an event for specific user
@app.route('/user/<username>/create_event/', methods=['POST'])
def create_event(username):
	if username in faux_usernames:
		start_time = request.form['start_time']
		end_time = request.form['end_time']
		event_id = generate_code()
		faux_users[username][event_id] = [start_time, end_time]
	url = '/user/' + username
	return redirect(url)

# deletes an event for a specific user
@app.route('/user/<username>/delete_event/<event_id>')
def delete_event(username,event_id):
	if username in faux_usernames:
		faux_users[username].pop(event_id)
	url = '/user/' + username
	return redirect(url)

# adds a user to a unique group
@app.route('/group/<group_code>/add_user', methods=['POST'])
def add_user(group_code):
	if group_code in faux_groups:
		username = request.form['username']
		if username in faux_usernames:
			faux_groups[group_code].append(username)
	url = '/group/' + group_code
	return redirect(url)

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)