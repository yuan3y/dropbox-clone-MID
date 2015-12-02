import requests
import os
import time
from filesmonitoring import runmonitoring
import filemeta

defaultpath =   "./store/"
# currentserver = "http://192.168.43.240"
currentserver = "http://127.0.0.1"
port = "5000"

filenames_list =  os.listdir(defaultpath)
print(filenames_list)

r = requests.get(currentserver+ ":" + port + "/getIndex", data={'path': defaultpath})
print(r)
# onserverfilemeta=r.json()['listfiles']
# onserverfolder_list=r.json()['listfolders']


# first of all send all files in dirs and subdirs to server
def walk(dir):
  for name in os.listdir(dir):
     path = os.path.join(dir, name)
     if os.path.isfile(path):
        file = open(path, 'r')
        data = file.read()
        file.close()
        r = requests.post(currentserver+ ":" + port + "/files", data={'filename': path, 'data':data, 'modification':'new'})
     if os.path.isdir(path):
        r = requests.post(currentserver+ ":" + port + "/folders", data={'dir': path, 'modification':'new'})
        walk(path)

walk(defaultpath)

# run script for determiming every changes in the folder
runmonitoring()






