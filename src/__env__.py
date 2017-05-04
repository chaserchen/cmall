from __future__ import unicode_literals, print_function, division
from veil.model.collection import *
from veil.profile.setting import *
from veil.frontend.nginx_setting import NGINX_PID_PATH

HTTP_SCHEME = 'http'
HTTPS_SCHEME = 'https'
HTTP_STANDARD_PORT = 80
HTTPS_STANDARD_PORT = 443

WEBSITES = [
    DictObject(purpose='cmall', prevents_xsrf=True, recalculates_static_file_hash=True, process_page_javascript=True, process_page_stylesheet=True,
               clears_template_cache=True),
    DictObject(purpose='operator', prevents_xsrf=True, recalculates_static_file_hash=True, process_page_javascript=True, process_page_stylesheet=True,
               clears_template_cache=True),
]


PERSON_WEBSITE_BUCKETS = ['captcha_image', 'cmall_images']

PERSON_WEBSITE_MAX_UPLOAD_FILE_SIZE = '3m'

REDIS_CLIENTS = ['persist_store', 'memory_cache']

POSTGRESQL_CLIENTS = ['cmall']

SECURITY_CONFIG = load_config_from(
    SECURITY_CONFIG_FILE,
    'db_user',
    'db_password',
    'db_owner',  # used for migration
    'db_owner_password',  # used for migration
    'sendgrid_username',
    'sendgrid_password',
    'hash_salt'  # used to hash password and secure cookie
)

LOGGING_LEVEL_CONFIG = objectify({
    'delayed_job_scheduler': 'info',
    'job_worker': 'info', # just control how pyres do the logging, our code still controlled by LOGGING_LEVEL_CONFIG.cmall
    'cmall_postgresql': {
        'log_min_duration_statement': 0 if VEIL_ENV.is_dev else 300
    },
    'cmall': {
        '__default__': 'DEBUG' if VEIL_ENV.is_dev or VEIL_ENV.is_test else 'INFO',
#        'cmall.feature': 'DEBUG',
    }
})


def env_config(
        cmall_website_start_port,
        cmall_website_process_count,
        cmall_website_domain,
        cmall_website_domain_port,
        operator_website_start_port,
        operator_website_process_count,
        operator_website_domain,
        operator_website_domain_port,
        persist_store_redis_host,
        persist_store_redis_port,
        memory_cache_redis_host,
        memory_cache_redis_port,
        cmall_postgresql_version,
        cmall_postgresql_host,
        cmall_postgresql_port,
        queue_type, queue_host,
        queue_port, resweb_domain,
        resweb_domain_port,
        resweb_host,
        resweb_port):
    return objectify(locals())


_resweb_program = resweb_program


def resweb_program(config):
    return _resweb_program(config.resweb_host, config.resweb_port, config.queue_host, config.queue_port)


def resweb_nginx_server(config):
    return nginx_server(config.resweb_domain, config.resweb_domain_port, {'/': nginx_reverse_proxy_location(config.resweb_host, config.resweb_port)})


_queue_program = queue_program


def queue_program(config):
    return _queue_program(config.queue_host, config.queue_port)


_delayed_job_scheduler_program = delayed_job_scheduler_program


def delayed_job_scheduler_program(config):
    return _delayed_job_scheduler_program(config.queue_host, config.queue_port, logging_level=LOGGING_LEVEL_CONFIG.delayed_job_scheduler)


def cmall_periodic_job_scheduler_program(config):
    return periodic_job_scheduler_program(LOGGING_LEVEL_CONFIG.cmall, application_config=cmall_config(config))

def cmall_job_worker_program(worker_name, queue_names, config, run_as=None, count=1, timeout=180):
    return job_worker_program(worker_name, LOGGING_LEVEL_CONFIG.job_worker, LOGGING_LEVEL_CONFIG.cmall, config.queue_host, config.queue_port,
        queue_names=queue_names, application_config=cmall_config(config), run_as=run_as, count=count, timeout=timeout)


def routines_job_worker_program(config, count=1):
    return cmall_job_worker_program('routines',
        [
            'rewrite_redis_aof',
            'clean_up_captcha_images',
            'clean_up_inline_static_files',
        ],
        config, count=count)


def transactional_email_worker_program(config, count=1):
    return cmall_job_worker_program('transactional_email', ['send_transactional_email'], config, count=count)


def postgresql_log_rotater_program(purpose):
    return log_rotater_program('{}_postgresql'.format(purpose), '* * * * *', {
        VEIL_LOG_DIR / '{}-postgresql'.format(purpose) / '*.csv': [
            'rotate 5',
            'size=50M',
            'missingok',
            'copytruncate'
        ]
    })


def log_rotated_postgresql_program(purpose, *args, **kwargs):
    if not VEIL_ENV.is_dev:
        kwargs['log_filename'] = 'postgresql.log' # will disable the builtin log rotation
    return merge_multiple_settings(postgresql_program(purpose, *args, **kwargs), postgresql_log_rotater_program(purpose))


def cmall_postgresql_program(config, more_config=None):
    more_config = more_config or {}
    return log_rotated_postgresql_program('cmall', config.cmall_postgresql_version, config.cmall_postgresql_host, config.cmall_postgresql_port,
        owner=SECURITY_CONFIG.db_owner, owner_password=SECURITY_CONFIG.db_owner_password,
        user=SECURITY_CONFIG.db_user, password=SECURITY_CONFIG.db_password,
        log_min_duration_statement=LOGGING_LEVEL_CONFIG.cmall_postgresql.log_min_duration_statement, **more_config)


def persist_store_redis_program(config):
    return redis_program('persist_store', config.persist_store_redis_host, config.persist_store_redis_port, persisted_by_aof=True)


def memory_cache_redis_program(config):
    return redis_program('memory_cache', config.memory_cache_redis_host, config.memory_cache_redis_port)


def cmall_website_programs(config):
    return website_programs('cmall', LOGGING_LEVEL_CONFIG.cmall, application_config=cmall_config(config), start_port=config.cmall_website_start_port,
        process_count=config.cmall_website_process_count)


def cmall_website_nginx_server(config, extra_locations=None):
    locations = website_locations('cmall', VEIL_ENV.is_prod or VEIL_ENV.is_staging, max_upload_file_size=PERSON_WEBSITE_MAX_UPLOAD_FILE_SIZE)
    locations = merge_multiple_settings(locations, extra_locations or {}, website_bucket_locations(PERSON_WEBSITE_BUCKETS))
    return nginx_server(config.cmall_website_domain, config.cmall_website_domain_port, locations=locations,
        upstreams=website_upstreams('cmall', config.cmall_website_start_port, config.cmall_website_process_count),
        error_page={'404': '404.html', '500': '500.html'}, error_page_dir='{}/static/cmall/error-page'.format(VEIL_HOME))


def operator_website_programs(config):
    return website_programs('operator', LOGGING_LEVEL_CONFIG.cmall, application_config=cmall_config(config), start_port=config.operator_website_start_port,
        process_count=config.operator_website_process_count)


def operator_website_nginx_server(config, extra_locations=None):
    locations = website_locations('operator', VEIL_ENV.is_prod or VEIL_ENV.is_staging, max_upload_file_size=PERSON_WEBSITE_MAX_UPLOAD_FILE_SIZE)
    locations = merge_multiple_settings(locations, extra_locations or {}, website_bucket_locations(PERSON_WEBSITE_BUCKETS))
    return nginx_server(config.operator_website_domain, config.operator_website_domain_port, locations=locations,
        upstreams=website_upstreams('operator', config.operator_website_start_port, config.operator_website_process_count),
        error_page={'404': '404.html', '500': '500.html'}, error_page_dir='{}/static/operator/error-page'.format(VEIL_HOME))


def nginx_log_rotater_program():
    return log_rotater_program('nginx', '* * * * *', {
        VEIL_LOG_DIR / 'nginx' / '*.log': [
            'rotate 5',
            'size=50M',
            'missingok',
            'notifempty',
            'sharedscripts',
            'postrotate',
            'if [ -f {} ]; then'.format(NGINX_PID_PATH),
            'kill -USR1 `cat {}`'.format(NGINX_PID_PATH),
            'fi',
            'endscript'
        ]
    })


def log_rotated_nginx_program(*args, **kwargs):
    return merge_multiple_settings(nginx_program(*args, **kwargs), nginx_log_rotater_program())


def cmall_config(config):
    cmall_config_ = objectify({
        'queue_client': {
            'type': config.queue_type,
            'host': config.queue_host,
            'port': config.queue_port
        },
        'sendgrid_client': {
            'username': SECURITY_CONFIG.sendgrid_username,
            'password': SECURITY_CONFIG.sendgrid_password
        },
        'hash': {
            'salt': SECURITY_CONFIG.hash_salt
        }
    })
    for purpose in REDIS_CLIENTS:
        cmall_config_['{}_redis_client'.format(purpose)] = {
            'host': config['{}_redis_host'.format(purpose)],
            'port': config['{}_redis_port'.format(purpose)]
        }
    cmall_website_authority = config.cmall_website_domain if 80 == config.cmall_website_domain_port else '{}:{}'.format(
        config.cmall_website_domain, config.cmall_website_domain_port)
    for purpose in PERSON_WEBSITE_BUCKETS:
        cmall_config_['{}_bucket'.format(purpose)] = {
            'type': 'filesystem',
            'base_directory': VEIL_BUCKETS_DIR / purpose.replace('_', '-'),
            'base_url': 'http://{}/buckets/{}'.format(cmall_website_authority, purpose.replace('_', '-')),
        }
    for purpose in POSTGRESQL_CLIENTS:
        cmall_config_['{}_database_client'.format(purpose)] = {
            'driver': 'veil.backend.database.postgresql',
            'type': 'postgresql',
            'host': config['{}_postgresql_host'.format(purpose)],
            'port': config['{}_postgresql_port'.format(purpose)],
            'database': purpose,
            'user': SECURITY_CONFIG.db_user,
            'password': SECURITY_CONFIG.db_password,
            'schema': 'public'
        }
    for website in WEBSITES:
        purpose = website.purpose
        cmall_config_['{}_website'.format(purpose)] = {
            'domain': config['{}_website_domain'.format(purpose)],
            'domain_port': config['{}_website_domain_port'.format(purpose)],
            'domain_scheme': config.get('{}_website_domain_scheme'.format(purpose), HTTPS_SCHEME if config['{}_website_domain_port'.format(purpose)] == HTTPS_STANDARD_PORT else HTTP_SCHEME),
            'start_port': config['{}_website_start_port'.format(purpose)],
            'locale': 'zh_Hans_CN.UTF-8',
            'master_template_directory': VEIL_HOME / 'src' / 'cmall' / 'website' / purpose,
            'prevents_xsrf': website.prevents_xsrf,
            'recalculates_static_file_hash': website.recalculates_static_file_hash,
            'process_page_javascript': website.process_page_javascript,
            'process_page_stylesheet': website.process_page_stylesheet,
            'clears_template_cache': website.clears_template_cache
        }
    return cmall_config_


def website_bucket_locations(purposes):
    locations = {}
    for purpose in purposes:
        bucket_base_directory = VEIL_BUCKETS_DIR / purpose.replace('_', '-')
        locations.update({'^~ /buckets/{}/'.format(purpose.replace('_', '-')): bucket_location(bucket_base_directory)})
    return locations
