# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

from veil.profile.model import *

db = register_database('cmall')


def get_shopper(id):
    return db().get('SELECT * FROM shopper WHERE id=%(id)s', id=id)


@command
def create_shopper(name=not_empty, mobile=is_mobile, email=is_email):
    db().insert('shopper', name=name, mobile=mobile, email=email)
