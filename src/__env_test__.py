from __future__ import unicode_literals, print_function, division
from veil_component import list_all_components
from veil.profile.setting import *
import __env__

TEST_SUPERVISOR_HTTP_PORT = 9091
TEST_REDIS_HOST = '127.0.0.1'
TEST_REDIS_PORT = 6380

config = __env__.env_config(
    cmall_website_start_port=2050,
    cmall_website_process_count=1,
    cmall_website_domain='cmall.com',
    cmall_website_domain_port=81,
    persist_store_redis_host=TEST_REDIS_HOST,
    persist_store_redis_port=TEST_REDIS_PORT,
    memory_cache_redis_host=TEST_REDIS_HOST,
    memory_cache_redis_port=TEST_REDIS_PORT,
    cmall_postgresql_version='9.5',
    cmall_postgresql_host='127.0.0.1',
    cmall_postgresql_port=5433,
    queue_type='immediate',
    queue_host='',  # no queue
    queue_port=0,
    resweb_domain='',  # no resweb
    resweb_domain_port=0,
    resweb_host='',
    resweb_port=0)

ENV_TEST = {
    'test': veil_env(name='test', hosts={}, servers={
        '@': veil_server(
            host_name='',
            sequence_no=20,
            supervisor_http_port=TEST_SUPERVISOR_HTTP_PORT,
            programs=merge_multiple_settings(
                redis_program('test', TEST_REDIS_HOST, TEST_REDIS_PORT),
                __env__.cmall_postgresql_program(config),
                __env__.log_rotated_nginx_program(merge_multiple_settings(
                    __env__.cmall_website_nginx_server(config),
                ))
            ),
            resources=[application_resource(component_names=list_all_components(), config=merge_settings(
                __env__.cmall_config(config), {
                    'test_bucket': {
                        'type': 'filesystem',
                        'base_directory': '',
                        'base_url': ''
                    }
                }
            ))]
        )
    })
}
