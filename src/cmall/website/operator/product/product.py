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
    products = list_products(category)
    products.sort(key=operator.attrgetter('brand'))
    categories = list_categories()
    return get_template('product-list-widget.html').render(products=products, current_category=category, categories=categories)


@template_filter('category_type')
def render_category_type(category):
    return PRODUCT_CATEGORIES[to_integer(category)]
