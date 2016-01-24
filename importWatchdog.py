
__author__ = 'falko'

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileModifiedEvent

import filesorter
import dmcutils

fsort = filesorter

class ImageFolderHandler(FileSystemEventHandler):

    def on_modified(self, event):
        if event.__class__.__name__ == "FileModifiedEvent":
            dmcutils.mylog("EventFired - FileModifiedEvent")
            fsort.processFile(event.src_path)




if __name__ == "__main__":

    dmcutils.init()
    fsort.init(dmcutils.commandarg)

    event_handler = ImageFolderHandler()

    observer = Observer()
    observer.schedule(event_handler, dmcutils.commandarg.inputFolder, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


