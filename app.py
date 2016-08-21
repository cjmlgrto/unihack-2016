from flask import Flask, render_template, request, redirect
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
	return render_template('index.html')

@app.route('/', methods=['POST'])
def login():
	username = request.form['username']
	if username != '':
		users = User.select()
		for user in users:
			if user.username == username:
				return redirect('/' + username)
		new_user = User.create(username=username)
		return redirect('/' + username)
	else:
		return render_template('index.html', error=True)

@app.route('/<username>')
def user(username=None):
	if username is not None:
		users = User.select()
		for user in users:
			if user.username == username:
				return render_template('user.html',username=user.username,schedule=user.schedule)
		return 'user not found!'
	else:
		return render_template('index.html', error=True)

if __name__ == '__main__':
	app.run(debug=True)