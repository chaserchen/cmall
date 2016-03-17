# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from veil.profile.web import *

from cmall.feature.product import *

operator_route = route_for('operator')


@widget
def list_title_promotions_widget():
    title_promotions = list_title_promotions()


@widget
def list_common_promotions_widget():
    common_promotions = list_common_promotions()

