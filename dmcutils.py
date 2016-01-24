__author__ = 'falko'

import hashlib
import argparse



def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFolder", help="Path to the folder to inspect") #TODO Add directory Validatoor -- https://stackoverflow.com/questions/11415570/directory-path-types-with-argparse
    parser.add_argument("targetFolder", help="Path to the image Directory")
    parser.add_argument("-n", "--copyonly", help="Do not move only copy files.",  action="store_true")
    parser.add_argument("-v", "--verbose", help="Turn on logging.", action="store_true")
    parser.add_argument("-re", "--requireExif", help="Skip all images with missing EXIF Timestamp", action="store_true")

    global commandarg
    commandarg = parser.parse_args()


def fileSha265Sum(file):
    f = open(file,'r')
    data = f.read()
    m = hashlib.sha256()
    m.update(data)
    return m.hexdigest()

def mylog(text):
    if(commandarg.verbose):
        print(text)