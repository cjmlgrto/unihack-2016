from flask import Flask
from models import *

app = Flask(__name__)

@app.before_request
def before_request():
	initialize_db()

@app.teardown_request
def teardown_request(exception):
	db.close()

@app.route('/')
def home():
	return 'Hello World'

@app.route('/create')
@app.route('/create/<username>')
def create(username=None):
	if username is None:
		return 'Error'
	else:
		new_user = User.create(username=username)
		return username + ' created!'

@app.route('/users')
def users():
	users_list = User.select()
	superstring = ''
	for user in users_list:
		superstring = superstring + str(user.username) + ', '
	return superstring


if __name__ == '__main__':
	app.run(debug=True)