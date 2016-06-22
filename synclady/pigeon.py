# -*- encoding: utf-8 -*-

import re
import time
import requests
import logging
import shutil
import subprocess

# Modules in Synclady
from conf import load_endpoints, LOG_FILENAME, get_source_local, get_source_server, get_source_server_path
ENDPOINTS = load_endpoints()

def dumpargs():
    """
        This decorator dumps out the arguments passed to a function before
        calling it
    """
    def decorate(func):
        argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
        fname = func.func_name
        def decorateDump(*args, **kargs):
            string = "Calling '" + fname + "' with args: " + ", ".join(
                                            '%s=%r' % entry
                                            for entry in zip(argnames, args[:len(argnames)])
                                        )
            print string

            ret = func(*args, **kargs)
            return ret

        return decorateDump
    return decorate

@dumpargs()
def rsync(event):
    """Rsyncs locally created files to server"""
    src = get_source_local()
    dest = get_source_server()
    subprocess.call(['rsync', '-avzr', '--exclude', '.*', src, dest])

    if event.event_type == "created" and not event.is_directory:
        print "Sending..."
        post_file_creation(event.src_path)

@dumpargs()
def post_file_creation(src):
    """Pings server API about file creation after file is present on server"""
    serv_src = clean_path(src)
    options = { 'path': serv_src }
    requests.post(ENDPOINTS['file_create'], params=options)

@dumpargs()
def post_folder_destroy(src):
    """Pings server about a folder destroy"""
    serv_src = clean_path(src)
    options = { 'path': serv_src }
    requests.post(ENDPOINTS['folder_destroy'], params=options)

@dumpargs()
def post_file_destroy(src):
    """Pings server about a file destroy"""
    serv_src = clean_path(src)
    options = { 'path': serv_src }
    requests.post(ENDPOINTS['file_destroy'], params=options)

def clean_path(path):
    """
        Converts to local path to server path
        Ex,
            localpath => '/Users/username/SHRINK/'
            serverpath => '/shrinkdata/username/'

            path => '/Users/username/SHRINK/A'
            newpath => '/shrinkdata/username/A'
    """
    local_path = get_source_local()
    server_path = get_source_server_path()
    return path.replace(local_path, server_path, 1)
