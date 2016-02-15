# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import veil_component

with veil_component.init_component(__name__):
    from .jd_shopping_mall import get_shopping_mall_phone_urls

    __all__ = [
        get_shopping_mall_phone_urls.__name__,
    ]
