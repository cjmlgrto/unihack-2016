from hello import db, Person

new = Person('john')
db.session.add(new)
db.session.commit()