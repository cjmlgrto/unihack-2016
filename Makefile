%default: run

run:
	rm -rf users.db
	open http://127.0.0.1:5000/
	python app.py