# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from veil.profile.web import *

from cmall.const import PROMOTION_COMMON
from cmall.feature.product import *

operator_route = route_for('operator')


@operator_route('GET', '/promotions')
def promotions_page():
    return get_template('promotions-page.html').render()


@operator_route('GET', '/common-promotions')
@widget
def common_promotions_widget():
    common_promotions = list_common_promotions()
    return get_template('common-promotions-widget.html').render(common_promotions=common_promotions)


@operator_route('POST', '/promotions')
def create_promotion_action():
    start_at = get_http_argument('start_at')
    end_at = get_http_argument('start_at')
    product_id = get_http_argument('product_id')
    type = get_http_argument('type', default=PROMOTION_COMMON)
    create_promotion(product_id, start_at, end_at, type)


@operator_route('DELETE', '/promotions/{{ id }}', id='\d+')
def delete_promotion_action():
    id = get_http_argument('id')
    delete_promotion(id)


@operator_route('GET', '/products/{{ product_id }}/promotion', product_id='\d+')
def get_product_promotion():
    product_id = get_http_argument('product_id')
    return get_template('product-promotion-widget.html').render(product_id=product_id)
