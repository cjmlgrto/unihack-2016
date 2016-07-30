# ---------------------------------
# Import Modules
# ---------------------------------
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# setup Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test02.db'
db = SQLAlchemy(app)

# ---------------------------------
# SQL Database
# ---------------------------------

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
	group_code = db.Column(db.Integer, unique=False)

	person_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, group_code, person_id):
		self.group_code = group_code
		self.person_id = person_id

# ---------------------------------
# HOME PAGE ROUTING
# ---------------------------------

# renders homepage
@app.route('/')
def home():
	return render_template('home.html')

# checks for username then renders homepage
@app.route('/', methods=['POST'])
def check_username():
	username = request.form['username']
	db_user = User.query.filter_by(name=username).first()
	if db_user is not None:
		return render_template('home.html', username_exists=True, username=username)
	else:
		return render_template('home.html', username_exists=False, username=username)

# ---------------------------------
# USERS ROUTING
# ---------------------------------

# renders a user's page
@app.route('/user/<username>')
def user(username):
	db_user = User.query.filter_by(name=username).first()
	if db_user is not None:
		events = eval(db_user.calendar)
		return render_template('user.html', username=username, events=events)
	else:
		return render_template('404.html', value=db_user)

# creates a new user and redirects to the new user page
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

# creates a new event for a specific user
@app.route('/user/<username>/create_event/', methods=['POST'])
def create_event(username):
	# create the event
	start = request.form['start']
	end = request.form['end']
	event = (start,end)

	# check if username in database
	db_user = User.query.filter_by(name=username).first()
	if db_user is not None:
		# insert event into row

		# redirect to user page
		url = '/user/' + username
		return redirect(url)
	else:
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

# adds a user to a unique group
@app.route('/group/<group_code>/add_user', methods=['POST'])
def add_user(group_code):
	if group_code in faux_groups:
		username = request.form['username']
		if username in faux_usernames:
			faux_groups[group_code].append(username)
	url = '/group/' + group_code
	return redirect(url)

# ---------------------------------
# Run Flask
# ---------------------------------

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
