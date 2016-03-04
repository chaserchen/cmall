# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

from veil.frontend.template import *
from veil.frontend.web import *

cmall_public_route = route_for('cmall', tags=(TAG_NO_LOGIN_REQUIRED,))


@widget
def shopper_website_nav_widget():
    return get_template('shopper-website-page.html').render()


@cmall_public_route('GET', '/')
def home_page():
    return get_template('shopper-website-page.html').render()
