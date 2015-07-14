# -*- coding: utf-8 -*-
'''Helper utilities and decorators.'''

from flask import flash, request, url_for


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)


'''
def thispage():
    try:
        ''
        print request.view_args.items(), request.args.to_dict().items()
        args = dict(request.view_args.items() + request.args.to_dict().items())
        args['thispage'] = '{path}?{query}'.format(
            path=request.path, query=request.query_string
        )
        return url_for(request.endpoint, **args)
    # pass for favicon
    except AttributeError:
        pass
'''
