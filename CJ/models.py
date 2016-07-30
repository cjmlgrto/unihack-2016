from flask_sqlalchemy import SQLAlchemy
from app import *

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
        return self.name

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	groupCode = db.Column(db.Integer, unique=False)
	person_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, groupCode, person_id):
		self.groupCode = groupCode
		self.person_id = person_id

	def __repr__(self):
		return self.groupCode