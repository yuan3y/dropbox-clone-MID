from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import requests

# class for monitoring FileSystem
class Handler(FileSystemEventHandler):

    #new file appeared -> send to server
    def on_created(self, event):
        print(event.src_path)
        file = open(event.src_path, 'r')
        data = file.read()
        file.close()
        requests.post("http://127.0.0.1:5000", data={'filename': event.src_path, 'data':data, 'modifiation':'new'})

    # deleting
    def on_deleted(self, event):
        requests.post("http://127.0.0.1:5000", data={'filename': event.src_path, 'modifiation':'del'})
        print (event)

    # renamimg
    def on_moved(self, event):
        print (event)
        file = open(event.dest_path, 'r')
        data = file.read()
        file.close()
        requests.post("http://127.0.0.1:5000", data={'filename': event.src_path, 'data':data, 'modifiation': 'mod', 'newfilename':event.dest_path})

    def on_modified(self, event):
        print (event)
        file = open(event.src_path, 'r')
        data = file.read()
        file.close()
        requests.post("http://127.0.0.1:5000", data={'filename': event.src_path, 'data':data, 'modifiation': 'upd'})

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