# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

from veil.frontend.cli import *
from veil.profile.model import *

from cmall.const import OPERATOR_COMMON

db = register_database('cmall')


@script('create-operator')
def create_operator_script(name, password, mobile, role):
    create_operator(name, password, mobile, role)


@command
def create_operator(name=not_empty, password=not_empty, mobile=is_mobile, role=optional(to_integer, default=OPERATOR_COMMON)):
    operator = get_operator_by_mobile(mobile)
    if operator:
        raise InvalidCommand({'operator': '您已注册，请直接登录'})
    db().insert('operator', name=name, password=get_password_hash(password), mobile=mobile, role=role)


@command
def operator_sign_in(mobile=is_mobile, password=not_empty):
    operator = get_operator_by_mobile(mobile)
    if not operator:
        raise InvalidCommand({'operator': '您还未注册'})
    if operator.password != get_password_hash(password):
        raise InvalidCommand({'password': '密码错误'})
    return operator


@command
def get_operator_by_mobile(mobile=is_mobile):
    return db().get('SELECT * FROM operator WHERE mobile=%(mobile)s', mobile=mobile)


def get_operator(id):
    return db().get('SELECT * FROM operator WHERE id=%(id)s', id=id)
