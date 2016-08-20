from peewee import *

db = SqliteDatabase('users.db')

class User(Model):
	id = PrimaryKeyField()
	username = CharField()

	class Meta:
		database = db

def initialize_db():
	db.connect()
	db.create_tables([User], safe=True)