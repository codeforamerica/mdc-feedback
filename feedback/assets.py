# -*- coding: utf-8 -*-
from flask_assets import Bundle, Environment

css = Bundle(
    "css/normalize.css",
    "css/skeleton.css",
    "css/jquery.raty.css",
    "css/remodal.css",
    "css/remodal-default-theme.css",
    "css/ie.css",
    "css/screen.css",
    output="public/css/common.css"
)

js = Bundle(
	"js/app.js"
)

assets = Environment()
test_assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
