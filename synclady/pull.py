# -*- encoding: utf-8 -*-

import logging
import subprocess

# Modules in Synclady
from synclady.shared import is_hidden
from conf import get_source_local, get_source_server

class Pull():

    @staticmethod
    def download():
        """
            Pull down everything in server to local
            IMP: Will delete anything stored previously
        """
        # Sync everything in server to local
        src = get_source_server()
        dest = get_source_local()
        subprocess.call(['rsync', '-avzr', '--exclude', '.*', '--delete-after', src, dest])
