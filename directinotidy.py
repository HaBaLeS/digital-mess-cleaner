from Queue import Queue
from thread import start_new_thread
import inotify.adapters
import filesorter
import dmcutils
import os

__author__ = 'falko'

filesfifo = Queue()
fsort = filesorter

def processQueue():
    while True:
        newFile = filesfifo.get()
        fsort.processFile(newFile)

def startinotify():
    i = inotify.adapters.InotifyTree(dmcutils.commandarg.inputFolder)
    for event in i.event_gen():
        if event is not None:
            (header, type_names, watch_path, filename) = event
            if "IN_CLOSE_WRITE" in type_names:
                filesfifo.put(os.path.join(watch_path,filename)     )


if __name__ == "__main__":
    dmcutils.init()
    fsort.init(dmcutils.commandarg)
    start_new_thread(processQueue, ())
    startinotify()
