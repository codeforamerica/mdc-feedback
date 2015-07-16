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
    filters='jsmin',
    output="public/js/common.js"
)
'''

css = Bundle(
    "css/style.css",
    "css/normalize.css",
    "css/skeleton.css",
    output="public/css/common.css"
)

js = Bundle(
	"js/app.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
