from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/check_username/', methods=['POST'])
def check_username():
	username = request.form['username']
	if username != 'bob':
		return username + ' is free!'
	else:
		return 'nope!'

if __name__ == '__main__':
	app.run(debug=True)