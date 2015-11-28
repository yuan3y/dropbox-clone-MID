import requests
import os
from client.filesmonitoring import filesmonitoring
import filemeta

defaultpath = "./store"
filenames_list =  os.listdir(defaultpath)
print(filenames_list)

# synhronise
for filename in filenames_list:
    filepath = defaultpath + filename
    if os.path.isfile(filepath):
        print(filepath)
        file = open(filepath, 'r')

        data = file.read()
        requests.post("http://127.0.0.1:5000", data={'filename': filename, 'data':data})
         # r2 = requests.post("http://127.0.0.1:5000", data=filemeta.filemeta(filename))

# look for changes in directory
runmonitoring()




