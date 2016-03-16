from __future__ import unicode_literals, print_function, division
import veil_component


with veil_component.init_component(__name__):
    __all__ = []

    def init():
        from veil.frontend.web import register_website_context_manager
        from veil.frontend.visitor import enable_visitor_origin_tracking
        from veil.frontend.visitor import enable_user_tracking
        from cmall.website.shartlet.user import set_current_shopper_on_request

        register_website_context_manager('cmall', enable_visitor_origin_tracking('cmall'))
        register_website_context_manager('cmall', enable_user_tracking('cmall', login_url='/login'))
        register_website_context_manager('cmall', set_current_shopper_on_request('cmall'))
