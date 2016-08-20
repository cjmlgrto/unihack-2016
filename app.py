from flask import Flask
from models import *

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello World'

@app.route('/create')
def create():
	return 'Create'

if __name__ == '__main__':
	app.run(debug=True)