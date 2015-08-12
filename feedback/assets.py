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
    "libs/bootstrap/dist/js/bootstrap.js",
    "js/plugins.js",
    
    filters='jsmin',
    output="public/js/common.js"
)

,
	output="public/js/common.js"

<script type="text/javascript" src="static/js/Chart.js"></script>
<script type="text/javascript" src="static/js/jquery.raty.js"></script>

'''

css = Bundle(
		"css/ie.css",
    "css/normalize.css",
    "css/skeleton.css",
    "css/jquery.raty.css",
    "css/remodal.css",
    "css/remodal-default-theme.css",
    "css/screen.css",
    output="public/css/common.css"
)

js = Bundle(
	
	"js/app.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
