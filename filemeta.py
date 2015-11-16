import requests
import os, time
from os.path import isfile, join, getsize
import hashlib
import json
import collections

def filehash(filepath):
    hash = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()


def filemeta(filepath):
    if os.path.isfile(filepath):
        return [('filename', filepath), ('timemodification', time.ctime(os.path.getmtime(filepath))), ('filesize', os.path.getsize(filepath)), ('hash', filehash(filepath))]
