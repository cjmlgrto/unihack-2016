from flask import Flask, render_template, request, redirect
from usernames import faux_usernames
from groups import faux_groups
from datetime import datetime

app = Flask(__name__)

# displays the home page
@app.route('/')
def home():
	return render_template('home.html')

# checks for username availability
@app.route('/login/', methods=['POST'])
def login():
	username = request.form['username']
	if username in faux_usernames:
		return render_template('home.html', username_exists=True, username=username)
	else:
		return render_template('home.html', username_exists=False, username=username)

# renders a user's page
@app.route('/user/<username>')
def user(username):
	if username in faux_usernames:
		return render_template('user.html', username=username)
	else:
		return username + " does not exist!"

# creates a new user's page
@app.route('/new_user/<username>')
def new_user(username):
	faux_usernames.append(username)
	return render_template('user.html', username=username)

if __name__ == '__main__':
	app.run(debug=True)