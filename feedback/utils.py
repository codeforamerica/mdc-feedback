# -*- coding: utf-8 -*-
'''Helper utilities and decorators.'''

import pytz

from flask import flash, request, url_for
from tzlocal import get_localzone

local_tz = get_localzone()


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)


def thispage():
    try:
        args = request.view_args.items().copy()
        args.update(request.args.to_dict().items())

        args['thispage'] = '{path}?{query}'.format(
            path=request.path, query=request.query_string
        )
        return url_for(request.endpoint, **args)
    # pass for favicon
    except AttributeError:
        pass


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)  # .normalize might be unnecessary
