import requests
import os
import time
from filesmonitoring import runmonitoring
import filemeta

defaultpath = "./store/"
filenames_list =  os.listdir(defaultpath)
print(filenames_list)

# synhronise
for filename in filenames_list:
    filepath = defaultpath + filename
    if os.path.isfile(filepath):
        print(filepath)
        file = open(filepath, 'r')
        data = file.read()
        file.close()
        requests.post("http://127.0.0.1:5000", data={'filename': filepath, 'data':data, 'modifiation':'new'})
         # r2 = requests.post("http://127.0.0.1:5000", data=filemeta.filemeta(filename))


while True:
    time.sleep(5)
    r = requests.get("http://127.0.0.1:5000/getnumfiles", data={'path': defaultpath})
    print(r.json)


# look for changes in directory
runmonitoring()






