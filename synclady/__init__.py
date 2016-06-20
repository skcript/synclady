# -*- encoding: utf-8 -*-
import os
import time
import yaml
import logging
import subprocess
from watch import FileWatch
from threading import Thread

# Modules in Synclady
from synclady.conf import LOG_FILENAME, load_config, update_config
from synclady.history import History
from synclady.pull import Pull

logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
log = logging.getLogger("synclady.init")

class Synclady():
    @staticmethod
    def pull():
        """Rewrites everything in locl to match server"""
        Pull.download()

    @staticmethod
    def sync():
        """Starts file listner"""
        FileWatch().start()

    @staticmethod
    def resync():
        """Resyncs server and local when local goes offline"""
        History().resync()
