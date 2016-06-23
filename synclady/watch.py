# -*- encoding: utf-8 -*-
import os
import re
import time
import shutil
import requests

from rq import Queue
from redis import Redis
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from conf import get_source_local

# Modules in Synclady
import synclady

class FileWatch(FileSystemEventHandler):
    def start(self):
        """Starts Watchdog file listener"""
        self.observer = Observer()
        path = synclady.conf.get_source_local()
        self.observer.schedule(self, path=path, recursive=True)
        self.observer.start()
        print "* Running Synclady at {0} (Press CTRL+C to quit)".format(path)

        try:
            while True:
                time.sleep(20)
                print "SYNCING FROM SERVER"
                synclady.Synclady.pull()
                print "END SYNCING FROM SERVER"
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def stop(self):
        """Stops Watchdog file listener"""
        self.observer.stop()

    def on_any_event(self, event):
        """Triggers on any event that Watchdog returns"""
        src = event.src_path
        # Events with hidden paths (dot files) are not registered
        if not synclady.shared.is_hidden(src):
            print "EVENT"
            synclady.pigeon.rsync(event)

    def on_deleted(self, event):
        """Triggers only on deleted events"""
        src = event.src_path
        if synclady.shared.is_hidden(src):
            # Events with hidden paths (dot files) are not registered
            return

        try:
            if event.is_directory:
                print "Deleted folder {0}".format(src)
                synclady.pigeon.post_folder_destroy(src)
            else:
                print "Deleted file {0}".format(src)
                synclady.pigeon.post_file_destroy(src)

        except Exception, e:
            print(e)
