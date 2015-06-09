import requests
import requests_cache
import time

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

requests_cache.install_cache(cache_name='github_cache', backend='sqlite', expire_after=180)

from models import Survey

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}

    hardcoded_api = 'https://api.typeform.com/v0/form/UYZYtI?key=433dcf9fb24804b47666bf62f83d25dbef2f629d&completed=true'
    if request.method == 'POST':
        print('POST method')
        now = time.ctime(int(time.time()))
        response = requests.get(hardcoded_api)
        print "Time: {0} / Used Cache: {1}".format(now, response.from_cache)


    return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
    app.run()

