# ---------------------------------
# Import Modules
# ---------------------------------
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# setup Flask
app = Flask(__name__)

# ---------------------------------
# SQL Database
# ---------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test4.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    calendar = db.Column(db.String)
    groups = db.relationship('Group', backref='user', lazy='dynamic')

    def __init__(self, name, calendar = ""):
        self.name = name
        self.calendar = calendar

    def __repr__(self):
        return self.name

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	groupCode = db.Column(db.Integer, unique=False)
	person_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, groupCode, person_id):
		self.groupCode = groupCode
		self.person_id = person_id

	def __repr__(self):
		return self.groupCode

# ---------------------------------
# Home Page
# ---------------------------------

# render homepage
@app.route('/')
def home():
	return render_template('home.html')

# check username availability
@app.route('/', methods=['POST'])
def check_username():
	# get data from form
	username = request.form['username']
	username_exists = None

	# query the database for a username
	db_user = User.query.filter_by(name=username).first()

	# set username_exists flag
	if db_user:
		username_exists = True
	else:
		username_exists = False

	# render homepage
	return render_template('home.html', username_exists=username_exists, username=username)

# ---------------------------------
# User Page
# ---------------------------------

# render user page
@app.route('/user/<username>')
def user(username):
	# query the database for a username
	db_user = User.query.filter_by(name=username).first()


	if username in users_database:
		events = users_database[username]
		return render_template('user.html', username=username, events=events)
	else:
		return render_template('404.html', value=username)

# create a new user page
@app.route('/new_user/<username>')
def new_user(username):
	# add the user to the database
	users_database[username] = []

	# redirect to newly created user page
	url = '/user/' + username
	return redirect(url)

# create a new event
@app.route('/user/<username>/create_event/', methods=['POST'])
def create_event(username):
	# ------------
	# NOTE: THIS NEEDS TO BE CHANGED AS THE CALENDAR UI IS INTEGRATED
	# ------------
	start = request.form['start']
	end = request.form['end']

	# append (start,end) to user's list of events
	users_database[username].append((start,end))

	# redirect to user page 
	url = '/user/' + username
	return redirect(url)

# delete a specific event
@app.route('/user/<username>/delete_event/<start>')
def delete_event(username, start):
	# find an event with a specific start date
	events = users_database[username]
	for index, value in enumerate(events):
		if str(value[0]) == start:
			# if the start date is found, delete this event
			events.pop(index)

	# redirect to user page 
	url = '/user/' + username
	return redirect(url)

# ---------------------------------
# Run Flask
# ---------------------------------

if __name__ == '__main__':
	app.run(debug=True)


