# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

import logging
from string import strip

import requests
from bs4 import BeautifulSoup
from veil.backend.database.client import *
from veil.backend.queue import *
from veil.frontend.cli import *
from veil.model.collection import *

from cmall.const import PRODUCT_CATEGORY_DIGITAL_PRODUCT, HEADERS_WWW, PRODUCT_CATEGORY_HOUSEHOLD_APPLIANCES

LOGGER = logging.getLogger(__name__)
queue = register_queue()
db = register_database('cmall')

ROOT_URL_DIGITAL_PRODUCT = 'http://www.smzdm.com/fenlei/diannaoshuma'
ROOT_URL_HOUSEHOLD_APPLIANCES = 'http://www.smzdm.com/fenlei/jiayongdianqi'

ROOTS = [
    DictObject(root_url=ROOT_URL_DIGITAL_PRODUCT, category=PRODUCT_CATEGORY_DIGITAL_PRODUCT),
    DictObject(root_url=ROOT_URL_HOUSEHOLD_APPLIANCES, category=PRODUCT_CATEGORY_HOUSEHOLD_APPLIANCES),
]


@script('create-product-urls')
def create_product_urls_script():
    for root in ROOTS:
        create_product_urls(root.root_url, root.category)


def create_product_urls(root_url, category):
    if not root_url:
        return
    try:
        response = requests.get(root_url, headers=HEADERS_WWW)
        response.raise_for_status()
    except Exception:
        LOGGER.exception('Got exception when request root url: %(root_url)s', {root_url: root_url})
        raise
    else:
        product_list_dom = BeautifulSoup(response.text)
        product_doms = product_list_dom.select('.card-wrap .pic-wrap a')
        if product_doms:
            product_urls = set(strip(product_dom.get('href')) for product_dom in product_doms if product_dom.get('href'))
            existing_product_urls = set(db().list_scalar('SELECT url FROM product_url WHERE category=%(category)s', category=category))
            new_product_urls = product_urls - existing_product_urls
            if new_product_urls:
                product_url_objects = [dict(url=product_url, category=category) for product_url in new_product_urls]
                db().insert('product_url', product_url_objects)
                print(product_url_objects)
