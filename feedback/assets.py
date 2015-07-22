# -*- coding: utf-8 -*-
from flask_assets import Bundle, Environment

'''
css = Bundle(
    "libs/bootstrap/dist/css/bootstrap.css",
    "css/style.css",
    filters="cssmin",
    output="public/css/common.css"
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/bootstrap/dist/js/bootstrap.js",
    "js/plugins.js",
    "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.9/jquery-ui.min.js",
    filters='jsmin',
    output="public/js/common.js"
)
'''

css = Bundle(
    "css/normalize.css",
    "css/skeleton.css",
    "css/style.css",
    output="public/css/common.css"
)

js = Bundle(
	"js/app.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
