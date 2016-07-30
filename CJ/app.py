# TODO -----------------
# [] Create event method- can only be implemented once the UI has been hooked up
# [] Delete event method- again, can only be implemented after UI integration
# [] Add users to a group
# [] Remove users to a group
# ----------------------

# --------------------
# Import modules

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# --------------------
# Initialise app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/users.db'
db = SQLAlchemy(app)

# --------------------
# Models for SQL

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    # The 'name' is really the code that is generated, however, it was left as name becuase i'm lazy
    firstName = db.Column(db.String(80))
    lastName = db.Column(db.String(80))
    calendar = db.Column(db.String)
    groups = db.relationship('Group', backref='user', lazy='dynamic')

    def __init__(self, name, calendar = '', firstName = '', lastName = ''):
        self.name = name
        self.calendar = calendar
        self.firstName = firstName
        self.lastName = lastName

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	group_code = db.Column(db.String, unique=False)
	person_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, group_code, person_id):
		self.group_code = group_code
		self.person_id = person_id

# --------------------
# Home page Routing

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/', methods=['POST'])
def check_username():
	username = request.form['username']
	db_user = User.query.filter_by(name=username).first()
	if db_user is not None:
		return render_template('home.html', username_exists=True, username=username)
	else:
		return render_template('home.html', username_exists=False, username=username)

# --------------------
# User page Routing

@app.route('/user/<username>')
def user(username):
	db_user = User.query.filter_by(name=username).first()
	if db_user is not None:
		events = eval(db_user.calendar)
		return render_template('user.html', username=username, events=events)
	else:
		return render_template('404.html', value=db_user)

@app.route('/new_user/<username>')
def new_user(username):
	db_user = User.query.filter_by(name=username).first()
	if db_user is None:
		new = User(username)
		db.session.add(new)
		db.session.commit()
		url = '/user/' + username
		return redirect(url)
	else:
		return render_template('404.html', value=username)

@app.route('/user/<username>/create_event/', methods=['POST'])
def create_event(username):
	url = '/user/' + username
	return redirect(url)

@app.route('/user/<username>/delete_event/<start>', methods=['POST'])
def delete_event(username):
	url = '/user/' + username
	return redirect(url)

# --------------------
# Group page Routing

@app.route('/group/<group_code>')
def group(group_code):
	groups = Group.query.filter_by(group_code=group_code).all()
	users = [i.user for i in groups]
	if users: # If users exist in this group
		return render_template('group.html', group_code=group_code, users=users)
	else:
		return render_template('404.html', value=group_code)

@app.route('/group/<group_code>/add_user', methods=['POST'])
def add_user(group_code):
	username = request.form['username']

	users = Group.query.filter_by(group_code=group_code).first()
	userids = [i.User.id for i in users]

	# Check to see if the user exists
	userid = User.query.filter_by(name=username).first()
	url = '/group/<group_code>'
	if userid is None:
		# The person they are trying to add does not exist
		return redirect(url)
	else:
		if userid in userids:
			return redirect(url)
			# The person is already in the group
		else:
			#Add to the group
			new_user = Group(group_code, userid)
			db.session.add(new_user)
			db.session.commit()
			return redirect(url)

@app.route('/group/<group_code>/remove_user/<username>')
def remove_user(group_code, username):
	user_get = User.query.filter_by(name=username).first()
	if user_get:
		# The user exists
		userid = user_get.id
		user = Group.query.filter_by(group_code='group_code', id=userid).first()
		db.session.delete(user)
		db.session.commit()
		return redirect('/group/<group_code>')

# --------------------
# Run the app

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)


