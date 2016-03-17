# -*- coding: UTF-8 -*-
from __future__ import unicode_literals, print_function, division

from veil.model.collection import DictObject

PRODUCT_CATEGORY_DIGITAL_PRODUCT = 1
PRODUCT_CATEGORY_HOUSEHOLD_APPLIANCES = 2
PRODUCT_CATEGORY_SPORT = 3
PRODUCT_CATEGORY_CLOTHES = 4
PRODUCT_CATEGORY_MOTHER = 5
PRODUCT_CATEGORY_RIYONGBAIHUO = 6
PRODUCT_CATEGORY_SHIPINBAOJIAN = 7
PRODUCT_CATEGORY_LIPINZHONGBIAO = 8
PRODUCT_CATEGORIES = DictObject([
    (PRODUCT_CATEGORY_DIGITAL_PRODUCT, '数码'),
    (PRODUCT_CATEGORY_HOUSEHOLD_APPLIANCES, '电器'),
    (PRODUCT_CATEGORY_SPORT, '户外'),
    (PRODUCT_CATEGORY_CLOTHES, '服装'),
    (PRODUCT_CATEGORY_MOTHER, '母婴'),
    (PRODUCT_CATEGORY_RIYONGBAIHUO, '百货'),
    (PRODUCT_CATEGORY_SHIPINBAOJIAN, '食品'),
    (PRODUCT_CATEGORY_LIPINZHONGBIAO, '礼品'),
])


HEADERS_WWW = {
    'Host': 'www.smzdm.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
}

HEADERS_WIKI = {
    'Host': 'wiki.smzdm.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
}


# three state constants for three-state variables
STATUS_VOID = 0  # 空的，无效的，未开始的
STATUS_INCOMPLETE = 1  # 部分的，不完全的，未完成的，进行中的
STATUS_COMPLETE = 2  # 全部的，完全的，完成的


operator_super = 1  # 超级管理员
operator_common = 2  # 普通管理员
