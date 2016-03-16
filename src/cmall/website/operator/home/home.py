# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from veil.profile.web import *

operator_route = route_for('operator')
operator_public_route = route_for('operator', tags=(TAG_NO_LOGIN_REQUIRED,))


@operator_public_route('GET', '/')
def home_page():
    return get_template('home-page.html').render()
