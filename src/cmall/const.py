# -*- coding: UTF-8 -*-
from __future__ import unicode_literals, print_function, division


GENDER_MALE = 1
GENDER_FEMALE = 2
GENDERS = {
    GENDER_MALE: '男',
    GENDER_FEMALE: '女'
}

PRODUCT_CATEGORY_DIGITAL_PRODUCT = 1
PRODUCT_CATEGORY_HOUSEHOLD_APPLIANCES = 2

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
