import os
import time

import requests
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import history
from client_default import *
from client_default import DEBUG
from filemeta import filemeta

# deleting files and folders
currentpathdel = currentserver + ":" + port + "/del"

# dependent changes
currentpathfiles = currentserver + ":" + port + "/files"
currentpathdirs = currentserver + ":" + port + "/folders"

# renaming files and folders
currentpathchange = currentserver + ":" + port + "/change"


# class for monitoring FileSystem
class Handler(FileSystemEventHandler):
    # new file appeared -> send to server
    def on_created(self, event):
        if observer_pause: pass
        path = event.src_path.replace('\\', '/')
        if os.path.isfile(path):
            # print(event.src_path)
            file = open(path, 'r')
            data = file.read()
            file.close()
            if DEBUG: print(currentpathfiles, 'filename', path, 'data', data, 'modification', 'new')
            requests.post(currentpathfiles, data={'filename': path, 'data': data, 'modification': 'new'})
        else:
            if DEBUG: print(currentpathdirs, 'dir', path, 'modification', 'new')
            requests.post(currentpathdirs, data={'dir': path, 'modification': 'new'})

    # deleting file/folder
    def on_deleted(self, event):
        if observer_pause: pass
        # no matter what to detele
        path = event.src_path.replace('\\', '/')
        if DEBUG: print(currentpathdel, 'dir', path, 'modification', 'del')
        requests.post(currentpathdel, data={'dir': path, 'modification': 'del'})

    # renamimg file/folder
    def on_moved(self, event):
        if observer_pause: pass
        data = ''
        path = event.src_path.replace('\\', '/')
        dest_path = event.dest_path.replace('\\', '/')
        if os.path.isfile(path):
            file = open(dest_path, 'r')
            data = file.read()
            file.close()
        if DEBUG: print(currentpathchange, 'previousName', path, 'data', data, 'modification', 'mod',
                        'newName', dest_path)
        requests.post(currentpathchange, data={'previousName': path, 'data': data, 'modification': 'mod',
                                               'newName': dest_path})

    # only for files
    def on_modified(self, event):
        if observer_pause: pass
        path = event.src_path.replace('\\', '/')
        if os.path.isfile(path):
            meta = filemeta(path)
            f = open('.index', 'r')
            servermeta = f.readline()
            servermeta = eval(servermeta)
            if path in servermeta and meta['hash'] == servermeta[path]['hash']:
                # print('no change for file '+str(meta))
                pass
            else:
                # print('it still changes')
                file = open(path, 'r')
                data = file.read()
                file.close()
                if DEBUG: print(currentpathfiles, 'filename', path, 'data', data, 'modification', 'upd')
                requests.post(currentpathfiles, data={'filename': path, 'data': data, 'modification': 'upd'})


# launch observer of filesystem
def runmonitoring():
    observer = Observer()
    observer.schedule(Handler(), path=defaultpath, recursive=True)
    observer.start()

    # run forever
    try:
        while True:
            #  check for scanges on the server
            global observer_pause
            observer_pause = True

            op_history = history.get_history()
            history.execute_history(op_history)
            # onserverfile_list, onserverfolder_list, deleted_files = writeIndex()
            #
            # #
            # # print
            # print(onserverfolder_list)
            # print(onserverfile_list)
            # print(deleted_files)
            #
            # for file in deleted_files:
            #     if (os.path.isfile(file)):
            #         os.remove(file)
            #     elif (os.path.exists(file)):
            #         shutil.rmtree(file)
            #
            # # create new folders
            # for dir in onserverfolder_list:
            #     if not os.path.exists(dir):
            #         os.makedirs(dir)
            #
            # for filename in onserverfile_list:
            #     if DEBUG: print(currentserver + ":" + port + "/getfile", "filename", filename)
            #     ri = requests.get(currentserver + ":" + port + "/getfile", data={'filename': filename})
            #     # print(ri)
            #     file = open(filename, 'w')
            #     data = ri.json()['data']
            #     file.write(data)
            #     file.close()
            # observer.join()
            time.sleep(2)
            observer_pause = False
            time.sleep(8)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
