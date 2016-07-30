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

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test8.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	calendar = db.Column(db.String)

	groups = db.relationship('Group', backref='user', lazy='dynamic')

	def __init__(self, name, calendar=''):
		self.name = name
		self.calendar = calendar

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
		events = db_user.calendar
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

# ---------------------------------
# Run Flask
# ---------------------------------

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)

