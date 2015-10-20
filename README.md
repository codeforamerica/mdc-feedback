# mdc-feedback
[MDC Fellowship 2015] Feedback Engine. Details TBA


### Development setup

This application is built on Flask and Python. The app.py file describes the models and routes.

A lot of early development for this application was based on this tutorial, so a lot of the environment configuration and staging/live set up is [based on these instructions](https://realpython.com/blog/python/flask-by-example-part-1-project-setup/). (For example, if you need to update the database models locally, use `python manage.py db migrate -m "Initial migration"`.) The production service lives on Heroku. Please contact us with any questions.

#### Requirements

* PostgreSQL Database - [How To](https://github.com/codeforamerica/howto/blob/master/PostgreSQL.md)
* Compass - [Get started with Compass](http://compass-style.org/)

#### A note on VIM

If you're not used to it see [VIM Adventures](http://vim-adventures.com/), because at least one of these steps requires using VIM.

#### Environmental variables

* `DATABASE_URL=[db connection string]` — My local example is `postgresql://localhost/feedback_dev`
* `CONFIG=[class name provided by config variable]` — I use `feedback.settings.DevelopmentConfig` for staging; for developer environments, see below

#### Project setup

* Set up a [virtual environment](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md)

* Use the following commands to bootstrap your development environment:
(kudos go to [Team Pittsburgh](https://github.com/codeforamerica/pittsburgh-purchasing-suite))

* After installing Compass, run `compass watch` inside your Compass directory, so that Compass will automatically compile your .scss files into .css.

* This repo uses Google Sheets as an information source for the 'what is this' UI on the dashboard. Tabletop.js is included in the repo, but you still need to publish your Sheet to web and replace the URL found in `dashboard.js` to enable this functionality.

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
* Upgrade your database in the virtual environment

```
python manage.py db upgrade
```

* Inside your virtual environment, open up the `postactivate` file:

```
vi $VIRTUAL_ENV/bin/postactivate
```

* Insert the following into your postactivate file:

```
export ADMIN_EMAIL='youremail@someplace.net'
export CONFIG="feedback.settings.DevelopmentConfig"
export DATABASE_URL="postgresql://localhost/feedback_dev"
```

* Reboot your virtual environment. (I use `workon mdc-feedback`, but your mileage will vary)

* Start the server

```
python manage.py server
```

* Visit `localhost:9000` in your browser to see the results
```
http://localhost:9000
```

### Deployment

Deployment is typically on Heroku. Follow [this tutorial](https://devcenter.heroku.com/articles/getting-started-with-python) for basic information on how to setup the project.

#### Environmental variables

#### Project setup

**email**:

The app uses [Flask-Mail](https://pythonhosted.org/Flask-Mail/) to handle sending emails. This includes emails about subscriptions to various contracts, notifications about contracts being followed, and others. In production, the app relies on [Sendgrid](https://sendgrid.com/), but in development, it uses the [Gmail SMTP server](https://support.google.com/a/answer/176600?hl=en). If you don't need to send emails, you can disable emails by setting `MAIL_SUPPRESS_SEND = True` in the `DevConfig` configuration object.

If you would like to send email over the Gmail SMTP server, you will need to add two environmental variables: `MAIL_USERNAME` and `MAIL_PASSWORD`.

**login and user accounts**

Right now, the app uses [persona](https://login.persona.org/about) to handle authentication. The app uses its own user database to manage roles and object-based authorization. You will need to sign in through persona and then enter yourself into the database in order to have access to admin and other pages.

A manage task has been created to allow you to quickly create a user to access the admin and other staff-only tasks. To add an email, run the following command (NOTE: if you updated your database as per above, you will probably want to give youself a role of 1, which will give you superadmin privledges), putting your email/desired role in the appropriate places:

```bash
python manage.py seed_user -e <your-email-here> -r <your-desired-role>
```

Now, logging in through persona should also give you access to the app.


### Tests

In order to run the tests, you will need to create a test database. You can follow the same procedures outlined in the install section. By default, the database should be named purchasing_test:

```
psql
create database feedback_test;
```

Tests are located in the feedback_test directory. To run the tests, run
```
PYTHONPATH=. nosetests feedback_test/
```
from inside the root directory. For more coverage information, run
```
PYTHONPATH=. nosetests feedback_test/ -v --with-coverage --cover-package=purchasing_test --cover-erase
```

### Migrations
Migrations are handled through [flask-migrate](https://github.com/miguelgrinberg/Flask-Migrate#flask-migrate)

Contacts
--------

* Ernie Hsiung
* Sophia Dengo
* Mathias Gibson

