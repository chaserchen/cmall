# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import logging
import requests
from veil.backend.database.client import *
from veil.backend.queue import *
from veil.backend.redis import *
from veil.frontend.cli import script
from bs4 import BeautifulSoup

from cmall.const import JD_PLATFORM, PRODUCT_TYPE_PHONE

LOGGER = logging.getLogger(__name__)
redis = register_redis('persist_store')
db = register_database('cmall')
queue = register_queue()


@script('get-shopping-mall-phone-urls')
def get_shopping_mall_phone_urls():
    get_shopping_mall_phone_urls_job()


@periodic_job('23 2 * * *')
def get_shopping_mall_phone_urls_job():
    root_url = 'http://channel.jd.com/shouji.html'
    try:
        response = requests.get(root_url)
    except Exception:
        LOGGER.exception('Goe exception when request root url: %(root_url)s', {root_url: root_url})
    else:
        soup = BeautifulSoup(response.text)
        jd_phone_urls = set(a['href'] for a in soup.select('.p-img > a') if a['href'].startswith('http://item.jd.com'))
        jd_phone_urls = list(set(jd_phone_urls).difference(set(db().list_scalar('SELECT url FROM product_urls'))))
        if jd_phone_urls:
            db().insert('product_urls', jd_phone_urls, url=lambda u: u, platform_id=JD_PLATFORM)
            for url in jd_phone_urls:
                queue().enqueue(get_product_data_job, url=url, product_type=PRODUCT_TYPE_PHONE)


@job('get_product_data')
def get_product_data_job(url, product_type):
    if db().has_rows('SELECT 1 FROM product_urls WHERE url=%(url)s', url=url):
        get_product_data(url, product_type)


@script('get-phone-data')
def get_product_data_script(url, product_type):
    if db().has_rows('SELECT 1 FROM product_urls WHERE url=%(url)s', url=url):
        get_product_data(url, product_type)


def get_product_data(url, product_type):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception:
        LOGGER.exception('Got exception when request url: %(url)s', {url: url})
    else:
        soup = BeautifulSoup(response.text)
        name = soup.select('.m-item-inner #name h1')[0].string
        blurb = soup.select('#p-ad')[0].string
        product_sku = soup.select('#short-share .fl span')[1].string
        price = requests.get('http://p.3.cn/prices/mgets?skuIds=J_' + product_sku).json()[0].get('p')
        detail_images = {index: image.get('src') for index, image in enumerate(soup.select('#spec-list .spec-items img'), start=1)}
        _get_product_data(blurb, detail_images, name, price, product_sku, url, product_type)


@transactional(db)
def _get_product_data(blurb, detail_images, name, price, product_sku, url, product_type):
    if not db().has_rows('SELECT 1 FROM shopping_mall WHERE platform_id=%(platform_id)s AND product_sku=%(product_sku)s AND price=%(price)s',
                         platform_id=JD_PLATFORM, product_sku=product_sku, price=price):
        db().insert('shopping_mall', platform_id=JD_PLATFORM, type=product_type, name=name, price=price, blurb=blurb, product_sku=product_sku,
                    detail_images=detail_images)
        db().execute('DELETE FROM product_urls WHERE url=%(url)s', url=url)
