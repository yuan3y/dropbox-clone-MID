import requests
import os
from os.path import isfile, join
'''
[ f for f in os.listdir('./') if isfile(join('./',f)) ]
'''

print(os.listdir("./"))
filenames_list =  os.listdir("./")

for filename in filenames_list:
    with open('./%s' % filename, 'r') as file:
        data = file.read()
        requests.post({'filename': filename, 'data':data})

payload = {'key1': 'value1', 'key2': 'value2'}
requests.post("http://127.0.0.1:5000", data=payload)
requests.post("http://127.0.0.1:5000", data=payload)