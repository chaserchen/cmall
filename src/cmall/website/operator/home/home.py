# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from veil.profile.web import *

from cmall.feature.shopper import *
from cmall.website.shartlet.user import remember_current_signed_in_shopper, get_current_operator

operator_route = route_for('operator')
operator_public_route = route_for('operator', tags=(TAG_NO_LOGIN_REQUIRED,))


@operator_public_route('GET', '/login')
def home_page():
    return get_template('login-page.html').render()


@operator_public_route('POST', '/login')
def sign_in_action():
    mobile = get_http_argument('mobile')
    password = get_http_argument('password')
    shopper = operator_sign_in(mobile, password)
    remember_current_signed_in_shopper(shopper, 'operator')


@widget
def nav_widget():
    operator = get_current_operator('operator')
    return get_template('nav-widget.html').render(operator=operator)


@operator_public_route('GET', '/logout')
def logout_action():
    remove_logged_in_user_id('operator')
    redirect_to('/')
