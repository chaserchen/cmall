# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

import logging
from string import strip

import requests
from bs4 import BeautifulSoup
from veil.backend.database.client import *
from veil.backend.queue import *
from veil.frontend.cli import *
from veil.model.binding import *
from veil.model.command import *

from cmall.const import HEADERS_WIKI

LOGGER = logging.getLogger(__name__)
db = register_database('cmall')
queue = register_queue()


@command
def create_platform_products(category=optional(to_integer)):
    if category:
        products = db().list('SELECT id, product_url FROM product WHERE category=%(category)s', category=category)
    else:
        products = db().list('SELECT id, product_url FROM product')
    if products:
        for product in products:
            queue().enqueue(create_platform_product_job, product_url=product.product_url, product_id=product.id)


@script('create-platform-product')
def create_platform_product_script(product_url, product_id):
    create_platform_product_job(product_url, product_id)


@job
def create_platform_product_job(product_url, product_id):
    try:
        response = requests.get(product_url, headers=HEADERS_WIKI)
        response.raise_for_status()
    except Exception:
        LOGGER.exception('Got exception when request product url: %(product_url)s', {product_url: product_url})
        raise
    else:
        platform_products = []
        product_dom = BeautifulSoup(response.text)
        platform_doms = product_dom.select('.mall_link dd')
        for platform_dom in platform_doms:
            name_dom = platform_dom.select('p.ellipsis')
            price_dom = platform_dom.select('p.mall_price .grey')
            url_dome = platform_dom.select('.go_buy_now')
            name = name_dom[0].string if name_dom else None
            name = strip(name) if name else None
            price = price_dom[0].string if price_dom else None
            price = strip(price) if price else None
            url = url_dome[0].get('href') if url_dome else None
            url = strip(url) if url else None
            platform_product = dict(name=name, product_id=product_id, price=price, url=url)
            platform_products.append(platform_product)
        print(platform_products)
