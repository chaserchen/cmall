# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

import contextlib

from veil.profile.web import *

from cmall.feature.shopper import *


def set_current_shopper_on_request(website):
    @contextlib.contextmanager
    def f():
        request = get_current_http_request()
        request.latest_shopper_id = get_latest_shopper_id(website)
        shopper = get_current_shopper(website)
        update_current_shopper_on_request(request, shopper)
        yield

    return f


def update_current_shopper_on_request(request, shopper):
    request.shopper = shopper
    request.shopper_id = shopper.id if shopper else None


def get_current_shopper_id(website):
    shopper_id = get_logged_in_user_id(website)
    return int(shopper_id) if shopper_id else None


def get_current_shopper(website):
    current_shopper_id = get_current_shopper_id(website=website)
    return get_shopper(current_shopper_id) if current_shopper_id else None


def get_latest_shopper_id(website):
    shopper_id = get_latest_user_id(website)
    return int(shopper_id) if shopper_id else 0


def remember_current_signed_in_shopper(current_shopper, website):
    remember_logged_in_user_id(website, current_shopper.id)


def remove_current_signed_in_shopper(website):
    remove_logged_in_user_id(website)


def get_current_operator(website):
    operator_id = get_logged_in_user_id(website)
    return get_operator(operator_id)
