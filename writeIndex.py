import requests

from client_default import defaultpath, currentserver, port


def writeIndex():
    r = requests.get(currentserver + ":" + port + "/getIndex", data={'path': defaultpath})
    onserverfilemeta = r.json()['listfiles']
    onserverfolder_list = r.json()['listfolders']
    print(onserverfilemeta)
    print(onserverfolder_list)
    f = open('.index', 'w')
    f.write(str(onserverfilemeta))
    f.close()
    return onserverfilemeta, onserverfolder_list