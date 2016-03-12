# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

from veil.profile.web import *

from cmall.feature.shopper import *


def get_current_shopper_id(website):
    shopper_id = get_logged_in_user_id(website)
    return int(shopper_id) if shopper_id else None


def get_current_shopper(website):
    shopper_id = get_logged_in_user_id(website)
    return get_shopper(shopper_id) if shopper_id else None
