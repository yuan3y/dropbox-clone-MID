import requests
import os, time
from os.path import isfile, join, getsize
'''
[ f for f in os.listdir('./') if isfile(join('./',f)) ]
'''

print(os.listdir("./"))
filenames_list =  os.listdir("./")
filter(os.path.isfile, os.listdir( os.curdir ))
# filter(os.path.isfile, filenames_list)

for filename in filenames_list:
    # with open('./%s' % filename, 'r') as file:
    #     data = file.read()
    #     requests.post({'filename': filename, 'data':data})
    requests.post("http://127.0.0.1:5000", data={'filename': filename, 'timemodification': time.ctime(os.path.getmtime(filename)), 'filesize': os.path.getsize(filename)})

# payload = {'key1': 'value1', 'key2': 'value2'}
# requests.post("http://127.0.0.1:5000", data=payload)
