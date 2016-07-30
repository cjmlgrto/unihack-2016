from flask import Flask, render_template, request, redirect, url_for
from usernames import faux_usernames
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DATABASE SETUP

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test3.db'
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
        return '<User %r>' % self.name

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	groupCode = db.Column(db.Integer, unique=False)
	person_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, groupCode, person_id):
		self.username = username
		self.email = email

	def __repr__(self):
		return '<User %r>' % self.username

# ROUTING 

# displays the home page
@app.route('/')
def home():
	return render_template('home.html')

# checks for username availability
@app.route('/', methods=['POST'])
def login():
	username = request.form['username']
	# replace with a query to the database for a username with the above.
	if username in faux_usernames:
		return render_template('home.html', username_exists=True, username=username)
	else:
		newUser = User(username)
		db.session.add(newUser)
		db.session.commit()
		return render_template('home.html', username_exists=False, username=username)

# renders a user's page
@app.route('/user/<username>')
def user(username):
	if username in faux_usernames:
		return render_template('user.html', username=username)
	else:
		return username + " does not exist!"

# creates a new user's page
@app.route('/new/<username>')
def new_user(username):
	faux_usernames.append(username)
	return render_template('user.html', username=username)

@app.route('/showallusers')
def show_all_users():
	return render_template('show_all.html', users = User.query.all() )

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
