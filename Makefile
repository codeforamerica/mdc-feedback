db.rebuild:
	rm -rf migrations
	dropdb feedback_dev
	createdb feedback_dev
	make db.init

db.init:
	python manage.py db init
	python manage.py db migrate
	python manage.py db upgrade

db.empty:
	dropdb feedback_dev
	createdb feedback_dev
	python manage.py db upgrade
	make load_from_socrata


deploy:
	git push heroku master

load_from_socrata:
	python ./feedback/scripts/pull_data.py
