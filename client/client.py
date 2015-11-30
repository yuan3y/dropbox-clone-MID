import requests
import os
import time
from filesmonitoring import runmonitoring
import filemeta

defaultpath = "./store/"
currentserver = "http://192.168.43.240"
port = "5000"

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
        r = requests.post(currentserver+ ":" + port, data={'filename': filepath, 'data':data, 'modification':'new'})
        print (r)
         # r2 = requests.post("http://127.0.0.1:5000", data=filemeta.filemeta(filename))


# while True:
#
#     r = requests.get("https://" + currentserver + ":" + port + "/getfiles", data={'path': defaultpath})
#     onserverfile_list = r.json()['list']
#     print(onserverfile_list)
#
#     for filename in onserverfile_list:
#         ri = requests.get("https://" + currentserver + ":" + port + "/getfile", data={'filename': filename})
#         print(ri)
#         file = open(defaultpath + filename, 'w')
#         data = ri.json()['data']
#         file.write(data)
#         file.close()
#
#     time.sleep(30)

# look for changes in directory

runmonitoring()






