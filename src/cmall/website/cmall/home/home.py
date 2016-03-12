# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

from veil.frontend.template import *
from veil.frontend.web import *

from cmall.website.shartlet.user import get_current_shopper

cmall_public_route = route_for('cmall', tags=(TAG_NO_LOGIN_REQUIRED,))


@cmall_public_route('GET', '/')
def home_page():
    return get_template('home-page.html').render()


@widget
def nav_widget():
    return get_template('nav-page.html').render()


@widget
def login_info_widget():
    shopper = get_current_shopper('cmall')
    return get_template('login-info-page.html').render(shopper=shopper)
