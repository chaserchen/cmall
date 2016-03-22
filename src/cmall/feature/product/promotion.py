# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from veil.profile.model import *

from cmall.const import PROMOTION_TITLE, PROMOTION_COMMON

db = register_database('cmall')


def list_title_promotions():
    return db().list('SELECT * FROM promotion WHERE type=%(PROMOTION_TITLE)s', PROMOTION_TITLE=PROMOTION_TITLE)


def list_common_promotions():
    return db().list('SELECT * FROM promotion WHERE type=%(PROMOTION_COMMON)s', PROMOTION_COMMON=PROMOTION_COMMON)


@command
def create_promotion(product_id=to_integer, start_at=to_date(format='%Y-%m-%d'), end_at=to_date(format='%Y-%m-%d'), type=to_integer):
    db().insert('promotion', product_id=product_id, start_at=start_at, end_at=end_at, type=type)


@command
def delete_promotion(id=to_integer):
    db().execute('DELETE FROM promotion WHERE id=%(id)s', id=id)
