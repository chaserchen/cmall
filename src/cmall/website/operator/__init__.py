from __future__ import unicode_literals, print_function, division

import veil_component

with veil_component.init_component(__name__):
    __all__ = []

    def init():
        from veil.frontend.web import register_website_context_manager
        from veil.frontend.visitor import enable_visitor_origin_tracking
        from veil.frontend.visitor import enable_user_tracking

        register_website_context_manager('operator', enable_visitor_origin_tracking('operator'))
        register_website_context_manager('operator', enable_user_tracking('operator', login_url='/login'))
