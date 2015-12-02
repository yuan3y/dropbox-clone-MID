import hashlib
import os
import time


def filehash(filepath):
    hash = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()


def filemeta(filepath):
    if os.path.isfile(filepath):
        return {'path': filepath, 'mtime': time.ctime(os.path.getmtime(filepath)), 'size': os.path.getsize(filepath),
                'hash': filehash(filepath)}
