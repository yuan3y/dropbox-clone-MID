from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import requests

# class for monitoring FileSystem
class Handler(FileSystemEventHandler):

    #new file appeared -> send to server
    def on_created(self, event):
        # print(event.src_path)
        file = open(event.src_path, 'r')
        data = file.read()
        requests.post("http://127.0.0.1:5000", data={'filename': event.src_path, 'data':data, 'modifiation':'new'})

    # deleting
    def on_deleted(self, event):
        requests.post("http://127.0.0.1:5000", data={'filename': event.src_path, 'data':'null', 'modifiation':'del'})
        # print (event)

    # renamimg
    def on_moved(self, event):
        file = open(event.dst_path, 'r')
        data = file.read()
        requests.post("http://127.0.0.1:5000", data={'filename': event.src_path, 'data':data, 'modifiation': 'mod', 'newfilename':event.dst_path})
        # print (event)

# launch observer of filesystem
def runmonitoring():
    observer = Observer()
    observer.schedule(Handler(), path="./store/", recursive=True)
    observer.start()

    #run forever
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()