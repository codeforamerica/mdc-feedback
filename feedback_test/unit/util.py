# -*- coding: utf-8 -*-

# See:
# https://github.com/codeforamerica/pittsburgh-purchasing-suite/blob/master/purchasing_test/unit/util.py

import datetime
from feedback.user.models import User

def create_a_user(email='foo@foo.com'):
    return User(email=email, first_name='foo', last_name='foo')

def insert_a_user(email='foo@foo.com'):
    user = create_a_user(email)
    user.save()
    return user
