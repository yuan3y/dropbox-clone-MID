import requests

from client_default import defaultpath, currentserver, port


def writeIndex():
    r = requests.get(currentserver + ":" + port + "/getIndex", data={'path': defaultpath})
    onserverfilemeta = r.json()['listfiles']
    onserverfolder_list = r.json()['listfolders']
    deleted_files = r.json()['deleted']
    # print(onserverfilemeta)
    # print(onserverfolder_list)
    # print(deleted_files)
    f = open('.index', 'w')
    f.write(str(onserverfilemeta))
    f.close()
    return onserverfilemeta, onserverfolder_list, deleted_files
