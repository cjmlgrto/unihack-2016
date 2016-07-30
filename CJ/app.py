from flask import Flask, render_template, request, redirect
from usernames import faux_usernames
from groups import faux_groups
from datetime import datetime
from base64 import b64encode

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
		return username + ' does not exist!'

# creates a new user's page
@app.route('/new_user/<username>')
def new_user(username):
	faux_usernames.append(username)
	return render_template('user.html', username=username)

# creates a new group
@app.route('/new_group/')
def new_group():
	group_code = generate_group_code()
	faux_groups.append(group_code)
	url = '/group/' + group_code
	return redirect(url)

# generates a group code
def generate_group_code():
	key = b64encode(str(hash(datetime.now())))
	return key

# renders a group page
@app.route('/group/<group_code>')
def group(group_code):
	if group_code in faux_groups:
		return render_template('group.html', group_code=group_code)
	else:
		return group_code + ' does not exist!'

if __name__ == '__main__':
	app.run(debug=True)