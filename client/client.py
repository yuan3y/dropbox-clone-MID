import os

import requests
from filesmonitoring import runmonitoring, writeIndex
from client_default import defaultpath, currentserver, port, DEBUG

ip_loc = "./.previous_ip"
if os.path.isfile(ip_loc):
    # start of client logic
    f = open(ip_loc, 'r')
    ip = f.readline()
    f.close()
    r = requests.post(currentserver + ":" + port + "/start", data={'path': defaultpath, 'type': 'restart', 'old_ip': ip})
    if DEBUG: print(currentserver + ":" + port + "/start", 'path', defaultpath, 'type', 'restart', 'old_ip', ip)
    ip = r.json()['ip']
    f = open(ip_loc, 'w')
    f.write(ip)
    f.close()
else:
    try:
        os.mkdir(defaultpath)
    except:
        pass

    r = requests.post(currentserver + ":" + port + "/start", data={'path': defaultpath, 'type': 'new'})
    if DEBUG: print(currentserver + ":" + port + "/start", 'path', defaultpath, 'type', 'new')
    ip = r.json()['ip']
    f = open(ip_loc, 'w')
    f.write(ip)
    f.close()

    server_filemeta, server_folder_list = writeIndex()
    if DEBUG: print(server_filemeta, server_folder_list)

    for folder in server_folder_list:
        try:
            os.mkdir(folder)
        except:
            pass

    for file in server_filemeta:
        ri = requests.get(currentserver + ":" + port + "/getfile", data={'filename': file})
        if DEBUG: print(currentserver + ":" + port + "/getfile", 'filename', file)
        file = open(file, 'wb')
        if ri is not None:
            try:
                data = ri.json()['data']
            except:
                data = ''
            file.write(data)
        file.close()


# run script for determiming every changes in the folder
runmonitoring()
