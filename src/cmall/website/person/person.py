# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from veil.profile.web import *
from cmall.feature.person import *

cmall_route = route_for('cmall')


@cmall_route('GET', '/')
def list_persons_page():
    return get_template('list-persons.html').render(persons=list_persons())
