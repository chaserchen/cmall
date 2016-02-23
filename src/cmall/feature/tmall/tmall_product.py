# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

import logging
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from veil.backend.database.client import *
from veil.backend.queue import *
from veil.frontend.cli import script
from veil.model.collection import *

from cmall.const import PRODUCT_CATEGORY_PHONE

LOGGER = logging.getLogger(__name__)
db = register_database('cmall')
queue = register_queue()


@script('get-tmall-phone-data')
def get_tmall_phone_data_script():
    get_tmall_phone_data_job()


@periodic_job('43 2 * * *')
def get_tmall_phone_data_job():
    root_url = 'https://list.tmall.com/search_product.htm?q=%D6%C7%C4%DC%CA%D6%BB%FA&click_id=%D6%C7%C4%DC%CA%D6%BB%FA&from=mallfp..pc_1.1_hq&spm=875.7789098.' \
               'a1z5h.2.Ur1Q2I'
    try:
        response = requests.get(root_url)
        response.raise_for_status()
    except Exception:
        LOGGER.exception('Got exception when request root url: %(root_url)s', {root_url: root_url})
        raise
    else:
        product_objects = []
        soup = BeautifulSoup(response.text)
        products = soup.select('.product')
        for p in products:
            if p:
                product_titles_dom = p.select('.productTitle a')
                stores_dom = p.select('.productShop .productShop-num')
                store_dom = p.select('.productShop .productShop-name')
                if product_titles_dom and (store_dom or stores_dom):
                    name = product_titles_dom[0].string
                    second_url = product_titles_dom[0].get('href')
                    second_url = 'https:{}'.format(second_url) if second_url else None
                    try:
                        item_response = requests.get(second_url)
                        item_response.raise_for_status()
                    except Exception:
                        LOGGER.exception('Got exception when request second url: %(second_url)s', {second_url: second_url})
                        raise
                    else:
                        item = BeautifulSoup(item_response.text)
                        detail_image_dom = item.select('#J_ImgBooth')
                    detail_image = detail_image_dom[0].get('src') if detail_image_dom else None
                    blurb = product_titles_dom[1].string if len(product_titles_dom) > 1 else None
                    if not stores_dom:
                        store_url = 'http:{}'.format(store_dom[0]['href'])
                        stores_url = None
                    else:
                        store_url = None
                        stores_url = 'http:{}'.format(stores_dom[0]['href'])
                    if name and detail_image:
                        product_objects.append(
                            DictObject(name=name, detail_image='http:{}'.format(detail_image), blurb=blurb, category=PRODUCT_CATEGORY_PHONE, store_url=store_url,
                                       stores_url=stores_url))
        products = [p for p in product_objects if not check_product_in_tmall_products(p.name)]
        db().insert('tmall_product', products)


def check_product_in_tmall_products(name):
    return db().has_rows('SELECT 1 FROM tmall_product WHERE name=%(name)s', name=name)
