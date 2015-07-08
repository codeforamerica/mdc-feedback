# mdc-feedback
[MDC Fellowship 2015] Feedback Engine. Details TBA


### Development setup

This application is built on Flask and Python. The app.py file describes the models and routes.

A lot of early development for this application was based on this tutorial, so a lot of the environment configuration and staging/live set up is [based on these instructions](https://realpython.com/blog/python/flask-by-example-part-1-project-setup/). (For example, if you need to update the database models locally, use `python manage.py db migrate -m "Initial migration"`.) The production service lives on Heroku. Please contact us with any questions.

#### Requirements

* PostgreSQL Database - [How To](https://github.com/codeforamerica/howto/blob/master/PostgreSQL.md)

#### A note on VIM

If you're not used to it see [VIM Adventures](http://vim-adventures.com/), because at least one of these steps requires using VIM. 

#### Environmental variables

* `DATABASE_URL=[db connection string]` — My local example is `postgresql://localhost/feedback_dev`
* `APP_SETTINGS=[]` — I use `config.StagingConfig` for staging

Set these up in a local `.env` file.

#### Project setup

* Set up a [virtual environment](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md)

* Use the following commands to bootstrap your development environment:

```
# clone the repo
git clone https://github.com/codeforamerica/mdc-feedback.git
# change into the repo directory
cd mdc-feedback
# install python dependencies
# NOTE: if you are using postgres.app, you will need to make sure to
# set your PATH to include the bin directory. For example:
# export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin/
pip install -r requirements.txt
```

* Set up a new database (not using Postgres.app): 

```
createdb feedback_dev
python app.py createdb
```

* On Mac OSX, using Postgres.app, and working within psql: 

```
CREATE USER user PASSWORD 'password';
CREATE DATABASE feedback_dev OWNER=user;
_Feel free to replace user and password with values of your choice._
```

* Inside your virtual environment, open up the `postactivate` file:

```
vi $VIRTUAL_ENV/bin/postactivate
```

* Insert the following into your postactivate file:

```
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://localhost/feedback_dev"
```

* Reboot your virtual environment. (I use `workon mdc-feedback`, but your mileage will vary)

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

