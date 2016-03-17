# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from veil.profile.model import *

from cmall.const import PROMOTION_TITLE, PROMOTION_COMMON

db = register_database('cmall')


def list_title_promotions():
    return db().list('SELECT * FROM promotion WHERE type=%(PROMOTION_TITLE)s', PROMOTION_TITLE=PROMOTION_TITLE)


def list_common_promotions():
    return db().list('SELECT * FROM promotion WHERE type=%(PROMOTION_COMMON)s', PROMOTION_COMMON=PROMOTION_COMMON)
