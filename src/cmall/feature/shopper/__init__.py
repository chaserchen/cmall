# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

import veil_component

with veil_component.init_component(__name__):
    from shopper import get_shopper

    __all__ = [
        get_shopper.__name__,
    ]
