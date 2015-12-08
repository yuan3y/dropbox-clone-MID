import os
import time

import requests
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import history
from client_default import DEBUG, currentserver, port, defaultpath
from fileindex import get_index
from filemeta import filemeta

# deleting files and folders

currentpathdel = currentserver + ":" + port + "/del"

# dependent changes
currentpathfiles = currentserver + ":" + port + "/files"
currentpathdirs = currentserver + ":" + port + "/folders"

# renaming files and folders
currentpathchange = currentserver + ":" + port + "/change"


def writeIndex():
    r = requests.get(currentserver + ":" + port + "/getIndex", data={'path': defaultpath})
    server_filemeta = r.json()['listfiles']
    server_folder_list = r.json()['listfolders']
    f = open('.index', 'w')
    f.write(str(server_filemeta))
    f.close()
    return server_filemeta, server_folder_list


def index_change():
    server_filemeta, server_folder_list = writeIndex()
    local_filemeta, local_folder_list = get_index(defaultpath)
    different_file = set(local_filemeta).difference(set(server_filemeta))
    different_folder = set(local_folder_list).difference(set(server_folder_list))
    local_removed_file = set(server_filemeta).difference(set(local_filemeta)).difference(different_file)
    local_removed_folder = set(server_folder_list).difference(set(local_folder_list)).difference(different_folder)
    return list(different_file), list(different_folder), list(local_removed_file), list(local_removed_folder)


# class for monitoring FileSystem
class Handler(FileSystemEventHandler):
    # new file appeared -> send to server
    def on_created(self, event):
        if observer_pause: pass
        path = event.src_path.replace('\\', '/')
        if os.path.isfile(path):
            # print(event.src_path)
            file = open(path, 'rb')
            data = file.read()
            file.close()
            if DEBUG: print(currentpathfiles, 'filename', path, 'modification', 'new')
            r = requests.post(currentpathfiles,
                              data={'filename': path, 'modification': 'new'},
                              files={'file': open(path, 'rb')})
            if DEBUG: print(r.text)
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
            file = open(dest_path, 'rb')
            data = file.read()
            file.close()
        if DEBUG: print(currentpathchange, 'previousName', path, 'data', type(data), len(data), 'modification', 'mod',
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
                file = open(path, 'rb')
                data = file.read()
                file.close()
                if DEBUG: print(currentpathfiles, 'filename', path, 'modification', 'upd')
                r = requests.post(currentpathfiles,
                                  data={'filename': path, 'modification': 'upd'},
                                  files={'file': open(path, 'rb')})
                if DEBUG: print(r.text)


# launch observer of filesystem
def runmonitoring():
    observer = Observer()
    observer.schedule(Handler(), path=defaultpath, recursive=True)
    observer.start()

    # run forever
    try:
        while True:
            #  check for changes on the server
            global observer_pause
            observer_pause = True

            op_history = history.get_history()
            history.execute_history(op_history)

            change_file, change_folder, local_removed_file, local_removed_folder = index_change()
            if DEBUG: print(change_file, change_folder)
            for path in change_folder:
                if os.path.isdir(path):
                    path = path.replace('\\', '/')
                    if DEBUG: print(currentpathdirs, 'dir', path, 'modification', 'new')
                    requests.post(currentpathdirs, data={'dir': path, 'modification': 'new'})
            for path in change_file:
                if os.path.isfile(path):
                    path = path.replace('\\', '/')
                    if DEBUG: print(currentpathfiles, 'filename', path, 'modification', 'new')
                    r = requests.post(currentpathfiles,
                                      data={'filename': path, 'modification': 'new'},
                                      files={'file': open(path, 'rb')})
                    if DEBUG: print(r.text)
            for path in local_removed_file:
                path = path.replace('\\', '/')
                if DEBUG: print(currentpathdel, 'dir', path, 'modification', 'del')
                requests.post(currentpathdel, data={'dir': path, 'modification': 'del'})

            for path in local_removed_folder:
                path = path.replace('\\', '/')
                if DEBUG: print(currentpathdel, 'dir', path, 'modification', 'del')
                requests.post(currentpathdel, data={'dir': path, 'modification': 'del'})
            time.sleep(2)
            observer_pause = False
            time.sleep(8)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
