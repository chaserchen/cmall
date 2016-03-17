# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

from veil.frontend.visitor import remember_logged_in_user_id
from veil.profile.model import *

db = register_database('cmall')


def get_shopper(id):
    return db().get('SELECT * FROM shopper WHERE id=%(id)s', id=id)


def get_shopper_by_mobile(mobile):
    return db().get('SELECT * FROM shopper WHERE mobile=%(mobile)s', mobile=mobile)


@command
def create_shopper(name=not_empty, password=not_empty, confirm_password=not_empty, mobile=is_mobile, email=optional(is_email)):
    if password != confirm_password:
        raise InvalidCommand({'password': '两次输入密码不一致'})
    elif get_shopper_by_mobile(mobile):
        raise InvalidCommand({'shopper': '您已注册，请直接登录'})
    else:
        return db().insert('shopper', returns_record=True, name=name, password=get_password_hash(password), mobile=mobile, email=email)


@command
def shopper_sign_in(mobile=is_mobile, password=not_empty):
    shopper = get_shopper_by_mobile(mobile)
    if not shopper:
        raise InvalidCommand({'shopper': '请先注册再登录'})
    elif shopper.password != get_password_hash(password):
        raise InvalidCommand({'password': '密码错误'})
    else:
        return shopper
