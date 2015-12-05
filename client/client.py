import os

import requests
from filesmonitoring import runmonitoring

from client_default import defaultpath, currentserver, port
from writeIndex import writeIndex

# currentserver = "http://192.168.43.240"

filenames_list = os.listdir(defaultpath)
print(filenames_list)

writeIndex()


# first of all send all files in dirs and subdirs to server
def walk(dir):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            file = open(path, 'r')
            data = file.read()
            file.close()
            r = requests.post(currentserver + ":" + port + "/files",
                              data={'filename': path, 'data': data, 'modification': 'new'})
        if os.path.isdir(path):
            r = requests.post(currentserver + ":" + port + "/folders", data={'dir': path, 'modification': 'new'})
            walk(path)


# walk(defaultpath)

# run script for determiming every changes in the folder
runmonitoring()
