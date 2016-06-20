# -*- encoding: utf-8 -*-

import re
import os
import logging
import subprocess

# Modules in Synclady
import synclady.pigeon
from synclady.shared import is_hidden
from conf import get_source_local, get_source_server

class History():
    @staticmethod
    def list():
        """Get list all files to be synced when system is offline"""

        src = get_source_local()
        dest = get_source_server()
        cmd = "rsync -nvai --exclude='.*/' {0} {1}".format(src, dest)

        historylist = os.popen(cmd).readlines()
        filelist = []

        for f in historylist:
            try:
                # TODO: Dev dependencies
                # path = f.split("SHRINK/")[1].replace("\n", "")
                # path = "Users/karthik/SHRINK/" + path

                # Rsync returns relative file paths with ownership info
                # appending to it, that occupies 10 characters
                path = f.replace(f[:10], '').replace("\n", "")
                path = "Users/karthik/SHRINK/" + path

                if not is_hidden(path) and os.path.isfile("/" + path):
                    filelist.append(path)
            except:
                print "Unable to process {0}".format(f)
                # print ""

        return filelist

    @staticmethod
    def push():
        """Pushes new files created to server"""
        filelist = History.list()
        src = get_source_local()
        dest = get_source_server()
        subprocess.call(['rsync', '-avzr', '--exclude ".*/"', src, dest])

        for filepath in filelist:
            # TODO: Dev dependencies
            print "Sending: "+filepath
            synclady.pigeon.post_file_creation("/" + filepath)

    @staticmethod
    def resync():
        """
            Syncs local and server. This pushes locally created files when offline
            to server. After, brings down files and directory structure in server
            to local.
            IMP: Does not remember files/folders deleted locally when offline.
        """
        # Sync everything in local to server without deleting
        # This will bring everything that's been created when offline to server
        # Will not sync anything that's been deleted
        History.push()

        # Sync everything in server to local
        # This will bring everything that's been created when offline to local
        # Will delete file/folders after syncing
        src = get_source_server()
        dest = get_source_local()
        subprocess.call(['rsync', '-avzr', '--delete-after', '--exclude ".*/"', src, dest])
