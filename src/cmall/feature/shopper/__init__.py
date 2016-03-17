# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

import veil_component

with veil_component.init_component(__name__):
    from shopper import get_shopper
    from shopper import get_shopper_by_mobile
    from shopper import create_shopper
    from shopper import shopper_sign_in

    from operator import get_operator
    from operator import get_operator_by_mobile
    from operator import create_operator
    from operator import operator_sign_in

    __all__ = [
        get_shopper.__name__,
        get_shopper_by_mobile.__name__,
        create_shopper.__name__,
        shopper_sign_in.__name__,

        get_operator.__name__,
        get_operator_by_mobile.__name__,
        create_operator.__name__,
        operator_sign_in.__name__,
    ]
