import requests
import os, time
from os.path import isfile, join, getsize
import hashlib
import filemeta

print(os.listdir("./"))
filenames_list =  os.listdir("./")
filter(os.path.isfile, os.listdir( os.curdir ))
# filter(os.path.isfile, filenames_list)


for filename in filenames_list:
    # with open('./%s' % filename, 'r') as file:
    #     data = file.read()
    #     requests.post({'filename': filename, 'data':data})
    if os.path.isfile(filename):
        requests.post("http://127.0.0.1:5000", data=filemeta.filemeta(filename))

# payload = {'key1': 'value1', 'key2': 'value2'}
# requests.post("http://127.0.0.1:5000", data=payload)