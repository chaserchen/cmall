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


@script('create-products')
def create_products_script():
    create_products()


@command
def create_products(category=optional(to_integer)):
    if category:
        product_url_objects = db().list('SELECT * FROM product_url WHERE category=%(category)s', category=category)
    else:
        product_url_objects = db().list('SELECT * FROM product_url')
    if product_url_objects:
        for product_url_object in product_url_objects:
            queue().enqueue(create_product_job, product_url=product_url_object.url, category=product_url_object.category)


@script('create-product')
def create_product_script(product_url, category):
    create_product_job(product_url, category)


@job
def create_product_job(product_url, category):
    if db().has_rows('SELECT 1 FROM product WHERE product_url=%(product_url)s', product_url=product_url):
        return
    try:
        response = requests.get(product_url, headers=HEADERS_WIKI)
        response.raise_for_status()
    except Exception:
        LOGGER.exception('Got exception when request product url: %(product_url)s', {product_url: product_url})
        raise
    else:
        product_dom = BeautifulSoup(response.text)
        name_dom = product_dom.select('title')
        title_dom = product_dom.select('.sub_title')
        brand_dom = product_dom.select('.a_underline')
        detail_image_dom = product_dom.select('.tab_big_img img')
        name = name_dom[0].string if name_dom else None
        title = title_dom[0].string if title_dom else None
        brand = brand_dom[1].string if len(brand_dom) > 1 else None
        detail_image = detail_image_dom[0].get('src') if detail_image_dom and detail_image_dom[0].get('src') else None
        name = strip(name) if name else None
        name = name.replace('_百科优选_什么值得买', '') if name and name.endswith('_百科优选_什么值得买') else name
        title = strip(title) if title else None
        brand = strip(brand) if brand else None
        detail_image = strip(detail_image) if detail_image else None
        if name and detail_image:
            save_product_data(name, category, product_url, title, brand, detail_image)


@command
def save_product_data(name=not_empty, category=to_integer, product_url=not_empty, title=anything, brand=anything, detail_image=anything):
    db().insert('product', name=name, category=category, product_url=product_url, title=title, brand=brand, detail_image=detail_image)
