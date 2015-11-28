import requests
import os
import filemeta
# import fileindex

print(os.listdir("./"))
filenames_list =  os.listdir("./")




for filename in filenames_list:
     if os.path.isfile(filename):
         file = open(filename, 'r')
         data = file.read()
         r1 = requests.post("http://127.0.0.1:5000", data={'filename': filename, 'data':data})
         r2 = requests.post("http://127.0.0.1:5000", data=filemeta.filemeta(filename))
         print (r1)
         print (r2)

# send request about index file
# r = requests.post('http://127.0.0.1:5000/', files={'.index': open('.index', 'r')})




