db.rebuild:
	rm -rf migrations
	dropdb feedback_dev
	createdb feedback_dev
	make db.init

db.init:
	python manage.py db init
	python manage.py db migrate
	python manage.py db upgrade
	python manage.py seed_roles

db.empty:
	dropdb feedback_dev
	createdb feedback_dev
	python manage.py db upgrade
	python manage.py seed_roles
	make load.users
	make load.stakeholders
	make load.surveys

deploy:
	git push heroku master

load.stakeholders:
	python manage.py seed_stakeholder -e ehsiung+r1@codeforamerica.org -s 1
	python manage.py seed_stakeholder -e ehsiung+r2@codeforamerica.org -s 2
	python manage.py seed_stakeholder -e ehsiung+r3@codeforamerica.org -s 3
	python manage.py seed_stakeholder -e ehsiung+r4@codeforamerica.org -s 4
	python manage.py seed_stakeholder -e 'ehsiung+r5@codeforamerica.org, ehsiung+r5b@codeforamerica.org' -s 5
	python manage.py seed_stakeholder -e ehsiung+r6@codeforamerica.org -s 6
	python manage.py seed_stakeholder -e ehsiung+r7@codeforamerica.org -s 7
	python manage.py seed_stakeholder -e ehsiung+r8@codeforamerica.org -s 8
	python manage.py seed_stakeholder -e ehsiung+r9@codeforamerica.org -s 9
	python manage.py seed_stakeholder -e ehsiung+r10@codeforamerica.org -s 10
	python manage.py seed_stakeholder -e ehsiung+r11@codeforamerica.org -s 11
	python manage.py seed_stakeholder -e ehsiung+r12@codeforamerica.org -s 12
	python manage.py seed_stakeholder -e ehsiung+r13@codeforamerica.org -s 13
	python manage.py seed_stakeholder -e ehsiung+r14@codeforamerica.org -s 14

load.users:
	python manage.py seed_user -e ehsiung@codeforamerica.org -r 1
	python manage.py seed_user -e sdengo@codeforamerica.org -r 1
	python manage.py seed_user -e mathias@codeforamerica.org -r 1
	python manage.py seed_user -e sarasti@miamidade.gov -r 1

load.surveys:
	python ./feedback/scripts/pull_data.py

send.report:
	python ./feedback/scripts/send_monthly_report.py

