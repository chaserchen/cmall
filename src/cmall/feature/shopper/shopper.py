# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

from veil.frontend.visitor import remember_logged_in_user_id
from veil.profile.model import *

db = register_database('cmall')


def get_shopper(id):
    return db().get('SELECT * FROM shopper WHERE id=%(id)s', id=id)


@command
def create_shopper(name=not_empty, password=not_empty, confirm_password=not_empty, mobile=is_mobile, email=optional(is_email)):
    if password != confirm_password:
        raise InvalidCommand({'password': '两次输入密码不一致'})
    else:
        return db().insert('shopper', returns_record=True, name=name, password=password, mobile=mobile, email=email)


@command
def sign_in(mobile=is_mobile, password=not_empty):
    shopper = db().get('SELECT * FROM shopper WHERE mobile=%(mobile)s AND password=%(password)s', mobile=mobile, password=password)
    if not shopper:
        raise InvalidCommand({'shopper': '请先登录再注册'})
    else:
        return shopper
