# mdc-feedback
[MDC Fellowship 2015] Feedback Engine. Details TBA


### Development setup

This application is built on Flask and Python. The app.py file describes the models and routes.

A lot of early development for this application was based on this tutorial, so a lot of the environment configuration and staging/live set up is [based on these instructions](https://realpython.com/blog/python/flask-by-example-part-1-project-setup/). (For example, if you need to update the database models locally, use `python manage.py db migrate -m "Initial migration"`.) The production service lives on Heroku. Please contact us with any questions.

#### Requirements

* PostgreSQL Database - [How To](https://github.com/codeforamerica/howto/blob/master/PostgreSQL.md)

#### Environmental variables

* `DATABASE_URL=[db connection string]` — My local example is `postgresql://localhost/feedback_dev`
* `APP_SETTINGS=[]` — I use `config.StagingConfig` for staging

Set these up in a local `.env` file.

#### Project setup

* Set up a [virtual environment](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md)

* Install the required libraries

```
$ pip install -r requirements.txt
```

* Set up a new database

```
createdb feedback_dev
python app.py createdb
```

* Start the server

```
python manage.py runserver
```

* Visit `localhost:5000` in your browser to see the results
```
http://localhost:5000
```

### Deployment

Deployment is typically on Heroku. Follow [this tutorial](https://devcenter.heroku.com/articles/getting-started-with-python) for basic information on how to setup the project.

#### Environmental variables

#### Project setup

### Tests

### Migrations
Migrations are handled through [flask-migrate](https://github.com/miguelgrinberg/Flask-Migrate#flask-migrate)

Contacts
--------

* Ernie Hsiung
* Sophia Dengo
* Mathias Gibson

