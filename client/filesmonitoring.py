from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time, requests,os

defaultpath = "./store/"
# currentserver = "http://192.168.43.240"
currentserver = "http://127.0.0.1"
port = "5000"

# deleting files and folders
currentpathdel = currentserver+ ":" + port + "/del"

# dependent changes
currentpathfiles = currentserver+ ":" + port + "/files"
currentpathdirs = currentserver+ ":" + port + "/folders"

# renaming files and folders
currentpathchange = currentserver+ ":" + port + "/change"

#

# class for monitoring FileSystem
class Handler(FileSystemEventHandler):

    #new file appeared -> send to server
    def on_created(self, event):
        if os.path.isfile(event.src_path):
            print(event.src_path)
            file = open(event.src_path, 'r')
            data = file.read()
            file.close()
            requests.post(currentpathfiles, data={'filename': event.src_path, 'data':data, 'modification':'new'})
        else:
            requests.post(currentpathdirs, data={'dir': event.src_path, 'modification':'new'})

    # deleting file/folder
    def on_deleted(self, event):
        # no matter what to detele
        requests.post(currentpathdel, data={'dir': event.src_path, 'modification':'del'})

    # renamimg file/folder
    def on_moved(self, event):
        data = ''
        if os.path.isfile(event.src_path):
            file = open(event.dest_path, 'r')
            data = file.read()
            file.close()
        requests.post(currentpathchange, data={'previousName': event.src_path, 'data':data, 'modification': 'mod', 'newName':event.dest_path})

    # only for files
    def on_modified(self, event):
        if os.path.isfile(event.src_path):
            file = open(event.src_path, 'r')
            data = file.read()
            file.close()
            requests.post(currentpathfiles, data={'filename': event.src_path, 'data':data, 'modification': 'upd'})

# launch observer of filesystem
def runmonitoring():
    observer = Observer()
    observer.schedule(Handler(), path=defaultpath, recursive=True)
    observer.start()

    #run forever
    try:
         while True:

             #  check for scanges on the server
             time.sleep(10)
             r = requests.get(currentserver+ ":" + port + "/getfiles", data={'path': defaultpath})
             print(r)

             # get directories and files on server
             onserverfolder_list = r.json()['listfolders']
             onserverfile_list = r.json()['listfiles']

             # print
             print(onserverfolder_list)
             print(onserverfile_list)

             # create new folders
             for dir in onserverfolder_list:
                 if not os.path.exists(dir):
                     os.makedirs(dir)

             # fill folders with new files
             for filename in onserverfile_list:
                ri = requests.get(currentserver+ ":" + port + "/getfile", data={'filename': filename})
                print(ri)
                file = open(filename, 'w')
                data = ri.json()['data']
                file.write(data)
                file.close()

    except KeyboardInterrupt:
        observer.stop()
    observer.join()