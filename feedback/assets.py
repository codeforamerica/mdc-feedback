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
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css",
    "css/style.css",
    output="public/css/common.css"
)
js = Bundle()

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
