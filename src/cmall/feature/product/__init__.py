# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

import veil_component

with veil_component.init_component(__name__):
    from .product_url import create_product_urls
    __all__ = [
        create_product_urls.__name__,
    ]
