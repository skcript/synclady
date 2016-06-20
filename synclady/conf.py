# -*- encoding: utf-8 -*-
import os
import re
import yaml
import redis
import logging

# Log configs
LOG_FILENAME = '/tmp/synclady.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
log = logging.getLogger("synclady.conf")

# Settings file
CONFIG_FILE = os.path.expanduser("~/synclady.yml")

def get_source_local():
    """Try to load local source"""
    if not os.path.isfile(CONFIG_FILE):
        return ""

    source = yaml.load(open(CONFIG_FILE))['source']
    if isinstance(source, dict):
        return source['local']
    else:
        return ""

def get_source_server():
    """Try to load server source"""
    if not os.path.isfile(CONFIG_FILE):
        return ""

    source = yaml.load(open(CONFIG_FILE))['source']
    if isinstance(source, dict):
        return "{0}:{1}".format(source['ip'], source['server'])
    else:
        return ""

def get_source_server_path():
    """Try to load server source"""
    if not os.path.isfile(CONFIG_FILE):
        return ""

    source = yaml.load(open(CONFIG_FILE))['source']
    if isinstance(source, dict):
        return source['server']
    else:
        return ""

def load_endpoints():
    """Try to load endpoints"""
    if not os.path.isfile(CONFIG_FILE):
        return {}

    endpoints = yaml.load(open(CONFIG_FILE))['endpoints']
    if isinstance(endpoints, dict):
        return endpoints
    else:
        return {}

def load_config(config_file=CONFIG_FILE):
    """Try to load YAML config file"""
    config = {'source': {}, 'endpoints': {}}
    if os.path.isfile(config_file):
        log.debug("Try loading config file: {0}".format(config_file))
        config = yaml.load(open(config_file)) or config
    else:
        log.debug("Try creating config file: {0}".format(config_file))
        open(config_file, 'w')

    return config

# Undocumented - Please do not use
def update_config(config, config_file=CONFIG_FILE):
    """Try to update YAML config file"""
    yaml.dump(config, open(config_file, "w"), default_flow_style=False)
    log.info("Updated config in %s" % CONFIG_FILE)
