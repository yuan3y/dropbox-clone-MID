from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import requests

defaultpath = "./store/"
currentserver = '192.168.56.1'
port = '5000'

# class for monitoring FileSystem
class Handler(FileSystemEventHandler):

    #new file appeared -> send to server
    def on_created(self, event):
        file = open(event.src_path, 'r')
        data = file.read()
        file.close()
        requests.post("https://" + currentserver + ":" + port, data={'filename': event.src_path, 'data':data, 'modifiation':'new'})

    # deleting
    def on_deleted(self, event):
        requests.post("https://" + currentserver + ":" + port, data={'filename': event.src_path, 'modifiation':'del'})

    # renamimg
    def on_moved(self, event):
        file = open(event.dest_path, 'r')
        data = file.read()
        file.close()
        requests.post("https://" + currentserver + ":" + port, data={'filename': event.src_path, 'data':data, 'modifiation': 'mod', 'newfilename':event.dest_path})

    def on_modified(self, event):
        file = open(event.src_path, 'r')
        data = file.read()
        file.close()
        requests.post("https://" + currentserver + ":" + port, data={'filename': event.src_path, 'data':data, 'modifiation': 'upd'})

# launch observer of filesystem
def runmonitoring():
    observer = Observer()
    observer.schedule(Handler(), path="./store/", recursive=True)
    observer.start()

    #run forever
    try:
        while True:
            #  check for scanges on the server
            time.sleep(10)
            r = requests.get("https://" + currentserver + ":" + port + "/getfiles", data={'path': defaultpath})
            onserverfile_list = r.json()['list']
            print(onserverfile_list)

            for filename in onserverfile_list:
                ri = requests.get("https://" + currentserver + ":" + port + "/getfile", data={'filename': filename})
                print(ri)
                file = open(defaultpath + filename, 'w')
                data = ri.json()['data']
                file.write(data)
                file.close()

    except KeyboardInterrupt:
        observer.stop()
    observer.join()