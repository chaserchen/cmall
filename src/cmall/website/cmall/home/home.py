# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

from veil.frontend.template import *
from veil.frontend.web import *

from cmall.feature.shopper import *
from cmall.website.shartlet.user import update_current_shopper_on_request, remember_current_signed_in_shopper, \
    remove_current_signed_in_shopper

cmall_public_route = route_for('cmall', tags=(TAG_NO_LOGIN_REQUIRED,))
cmall_route = route_for('cmall')


@cmall_public_route('GET', '/')
def home_page():
    return get_template('home-page.html').render()


@widget
def nav_widget():
    return get_template('nav-page.html').render()


@widget
def shopper_name_widget():
    shopper = get_current_http_request().shopper
    return get_template('shopper-name-widget.html').render(shopper=shopper)


@cmall_public_route('GET', '/register')
def register_widget():
    return get_template('register-widget.html').render()


@cmall_public_route('GET', '/login')
def login_widget():
    return get_template('login-widget.html').render()


@cmall_public_route('POST', '/register')
def create_shopper_action():
    request = get_current_http_request()
    name = get_http_argument('name')
    password = get_http_argument('password')
    confirm_password = get_http_argument('confirm_password')
    mobile = get_http_argument('mobile')
    email = get_http_argument('email')
    shopper = create_shopper(name=name, password=password, confirm_password=confirm_password, mobile=mobile, email=email)
    update_current_shopper_on_request(request, shopper)
    remember_current_signed_in_shopper(shopper, 'cmall')


@cmall_public_route('POST', '/login')
def login_action():
    request = get_current_http_request()
    mobile = get_http_argument('mobile')
    password = get_http_argument('password')
    shopper = shopper_sign_in(mobile, password)
    update_current_shopper_on_request(request, shopper)
    remember_current_signed_in_shopper(shopper, 'cmall')


@cmall_public_route('GET', '/logout')
def logout_action():
    remove_current_signed_in_shopper('cmall')
