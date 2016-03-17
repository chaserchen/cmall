# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

import operator
from veil.profile.web import *

from cmall.const import PRODUCT_CATEGORIES
from cmall.feature.product import *

operator_route = route_for('operator')


@operator_route('GET', '/')
def list_product_page():
    return get_template('product-list-page.html').render()


@operator_route('GET', '/products')
@widget
def list_product_widget():
    category = get_http_argument('category', to_type=int, default=1)
    show_hide_products = get_http_argument('show_hide_products', to_type=to_bool, default=False)
    if show_hide_products:
        products = list_hide_products()
    else:
        products = list_products(category)
    categories = list_categories()
    return get_template('product-list-widget.html').render(products=products, current_category=category, categories=categories,
                                                           show_hide_products=show_hide_products)


@template_filter('category_type')
def render_category_type(category):
    return PRODUCT_CATEGORIES[to_integer(category)]


@operator_route('PUT', '/hide-product')
def hide_product_action():
    product_id = get_http_argument('product_id')
    hide_product(product_id)


@operator_route('PUT', '/show-product')
def show_product_action():
    product_id = get_http_argument('product_id')
    show_product(product_id)
