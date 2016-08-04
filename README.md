# Miami-Dade County Feedback Engine

## What is this?

Feedback Engine takes input from either a Typeform survey or a TextItIn user flow, normalizes the data into a database, sends follow-up emails to section division stakeholders and provide real-time analytics for both county employees and members of the public as an attempt to increase "feedback agility."

See the [Miami-Dade County Summit Presentation](https://www.youtube.com/watch?list=PL65XgbSILalUZFyWsZqbtZKN1iffAOM5M&v=DLFItyzBvhQ) for a five minute video explaining the context.

## Who made it?

The 2015 Miami-Dade County Fellowship Team, with feedback input from Michael Sarasti (Miami-Dade County Communications), Crista Erml-Martinez (Miami-Dade County RER) and Donna Romito (Miami-Dade County RER).

Thanks to the following 2015 Fellows for implementation input: Ben Smithgall (Team Pittsburgh), Ben Golder (Team Richmond VA)

Status: Limited Alpha

## How did we build this?

### Colophon

Repo: [https://github.com/codeforamerica/mdc-feedback](https://github.com/codeforamerica/mdc-feedback)

Python 2.4 (Flask), postgres, heroku

Survey APIs: Typeform, TextIt.In

### Core Dependencies

The suite is a [Flask](http://flask.pocoo.org/) app. It uses [Postgres](http://www.postgresql.org/) for a database and uses bower to manage most of its dependencies. It also uses less to compile style assets. In production, the project uses Celery with Redis as a broker to handle backgrounding various tasks. Big thanks to the cookiecutter-flask project for a nice kickstart.

It is highly recommended that you use use [virtualenv](https://readthedocs.org/projects/virtualenv/) (and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) for convenience). For a how-to on getting set up, please consult this [howto](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md). Additionally, it is recommended that you use [postgres.app ](http://postgresapp.com/)to handle your Postgres (assuming you are developing on OSX).

### Installation and setup

#### Quick local installation using Make

 First, create a virtualenv and activate it. Then:

```
git clone git@github.com:codeforamerica/mdc-feedback.git

# create the 'feedback_dev' database
psql -c 'create database feedback_dev;'

# set environmental variables - it is recommended that you set these for your
# your virtualenv, using a tool like autoenv or by modifying your activate script
# export.

# If you used virtualenvwrapper you can use the command
# vi $VIRTUAL_ENV/bin/postactivate .

export ADMIN_EMAIL='youremail@someplace.net'
export CONFIG=feedback.settings.DevelopmentConfig
export PYTHONPATH='.'
export MAIL_USERNAME="[YOUR-DEVELOPMENT-GMAIL-ADDRESS]"
export MAIL_PASSWORD="[YOUR-PASSWORD]"
export TYPEFORM_KEY="b903e7c38f9ae29378f24b69eb743330d9dee34d"
export TEXTIT_KEY="41a75bc6977c1e0b2b56d53a91a356c7bf47e3e9"

# this next command will do all installs, add tables to the database,
# and insert seed data (note that this needs an internet connection to
# scrape data from Typeform and TextIt.in)
make setup

# start your server
python manage.py server
```

#### More detailed installation instructions

If you want to walk through the complete setup captured above in make setup, use the following commands to bootstrap your development environment:

#### python app:

```
# clone the repo
git clone https://github.com/codeforamerica/mdc-feedback

# change into the repo directory
cd mdc-feedback

# install python dependencies
# NOTE: if you are using postgres.app, you will need to make sure to
# set your PATH to include the bin directory. For example:
# export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin/
# note, if you are looking to deploy, you won't need dev dependencies.
# uncomment & run this command instead:
# pip install -r requirements.txt
```

NOTE: The [app's configuration lives in settings.py](https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/settings.py). When different configurations (such as DevConfig) are referenced in the next sections, they are contained in that file.

#### E-mails

The app uses [Flask-Mail](https://pythonhosted.org/Flask-Mail/) to handle sending emails. This includes emails about subscriptions to various contracts, notifications about contracts being followed, and others. In production, the app relies on [Sendgrid](http://www.sendgrid.com), but in development, it uses the [Gmail SMTP server](https://support.google.com/a/answer/176600?hl=en). If you don't need to send emails, you can disable emails by setting `MAIL_SUPPRESS_SEND = True` in the DevConfig configuration object.

If you would like to send email over the Gmail SMTP server, you will need to add two environmental variables: `MAIL_USERNAME` and `MAIL_PASSWORD`.

#### Database

Once you've created your database, you'll need to open feedback/settings.py and edit the DevConfig object to use the proper [SQLAlchemy database configuration string](http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#postgresql). If you named your database feedback_dev, you probably won't have to change anything. Then:

## upgrade your database to the latest version

```
python manage.py db upgrade
```

By default, SQLAlchemy logging is turned off. If you want to enable it, you'll need to add a SQLALCHEMY_ECHO flag to your environment.

#### Login

Right now, the app [uses persona to handle authentication](https://login.persona.org/about). The app uses its own user database to manage roles and object-based authorization, and the email used for sign in is whitelisted against the CITY_DOMAINS settings variable. You will need to sign in through persona and then enter yourself into the database in order to have access to admin and other pages.

A manage task has been created to allow you to quickly create a user to access the admin and other staff-only tasks. To add an email, run the following command (NOTE: if you updated your database as per above, you will probably want to give yourself a role of 1, which will give you admin privileges), putting your email/desired role in the appropriate places:

```
python manage.py seed_user -e <your-email-here> -r <your-desired-role>
```

#### Seeding Data

If you boot up the app immediately after installing the app, it will have no data. If you want to add some data, the makefile script "make load_surveys " has been added to allow for quick data importation.

#### The Current Staging Environment on Heroku

##### Resources

##### Environment Variables

* `BROWSERID_URL` (Necessary for Mozilla persona)
* `CONFIG` (Set to feedback.settings.StagingConfig)
* `DATABASE_URL`
* `SENDGRID_PASSWORD`
* `SENDGRID_USERNAME`
* `SERVER_NAME` (Necessary for the timed e-mail template task; it’s `BROWSERID_URL` without the http or https)
* `TYPEFORM_API`
* `TEXIT_API`

### Miscellaneous Stuff

#### Database Tables

* `survey`: contains a standardized version of all surveys
* `roles`: contains a list of rules, seeded manually by python manage.py seed_roles
* `users`: A list of users that have accounts. Primary key is e-mail address and contains the ID number of the roles table.
* `stakeholders`: A string consisted of comma separated e-mail addresses.
* `monthly-report`: A string consisted of comma separated e-mail addresses which will receive the monthly report. As of now, only one row.

#### Server-based Scripts

##### Non-Timed

* Seed User: `python manage.py seed_user -e <your-email-here> -r <your-desired-role>`

* Seed Roles: `python manage.py seed_roles`

* Seed Stakeholder: `python manage.py seed_stakeholder -e <your-email-here> -s <section-number-as-integer>`

##### Timed

We used Heroku’s scheduler to run a couple of tasks. Heroku recommended using the scheduler over the standard cron job functionality - if you move to AWS that may be a more appropriate option.

* `make load.surveys` (Hourly) - checks survey APIs for new entries. If so, they are added to the surveys database table. Additionally, if there are new surveys marked for follow-up, they are assigned to the e-mails in the stakeholders table.

* `make send.report` (Monthly) - creates a monthly status report. E-mailed to addresses listed in the monthly-report table.

#### Front-End

* Front-end Framework: Skeleton, jQuery
* Fonts: Railway
* Charts: ChartsJS

## Basic Outline for Building Out Surveys

### Overview:

* **Create your quiz in Typeform and/or TextIt.**

Typeform is the platform we used to create web based surveys. Code For America has a PRO account that lets us use logic jumps which is how we handle English and Spanish versions of the quiz. (You could probably get around this by importing multiple sources, but you’ll need to [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) it.)

We use TextItIn for SMS interfaces.  Needless to say, make sure the questions for the surveys match between the SMS and Web versions and the English and Spanish versions.

* **Make sure the survey model has the right fields for every survey question.**

Make sure you use the python manage.py db migrate and python manage.py db upgrade commands to make sure the table is right.


* **Make sure you change the appropriate constants. **

If you are going to use a different Typeform / TextIt quiz than what is included, you’ll need to modify the API URLs and API keys that the APIs use. These are housed at [https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/surveys/constants.py](https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/surveys/constants.py), with some constants at [https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/scripts/pull_data.py](https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/scripts/pull_data.py).

If you’re building a multilingual quiz, normalize the text to constants.

Typeform questions are given a dynamic id through the API. The TF constant is a dictionary mapping values to more consistent names.

* **Build any necessary components to normalize the different quiz results into your database format. **

The etl_web_data and etl_sms_data functions at [https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/scripts/pull_data.py](https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/scripts/pull_data.py) contain the ETL.

The resultant data is checked against a schema inside the load_data method. For this we used marshmallow, a tool which serializes data and a special flavor which matches and verifies the schema to a model and filters out existing models. The schema code is at [https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/surveys/serializers.py](https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/surveys/serializers.py). If all is valid it’ll write the results to the database.

* **Customize the dashboard widgets to display the appropriate metric. **The majority of the front page dashboard code is at [https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/dashboard/views.py](https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/dashboard/views.py) . The template is at [https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/templates/public/home.html](https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/templates/public/home.html) and functions to get related data are at [https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/dashboard/vendorsurveys.py](https://github.com/codeforamerica/mdc-feedback/blob/master/feedback/dashboard/vendorsurveys.py) .

### Beyond the Scope of this Project

* We could be better about cleaning up our front-end Javascript libraries using a build system like grunt, gulp or bower.

* Unit tests. Enough said.

* We used two separate platforms for SMS and Web versions, and then had to account for English and Spanish versions of the survey. There’s no reason why we couldn’t use a JSON file in-house and generate the Web survey (via Typeform.IO) or the SMS survey (via something like Twilio) dynamically.

