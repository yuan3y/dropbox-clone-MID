import os
import shutil

import requests
from client_default import defaultpath, currentserver, port, DEBUG


def get_history():
    r = requests.get(currentserver + ":" + port + "/getHistory", data={'path': defaultpath})
    # print(r.json())
    op_history = r.json()['history']
    return op_history


def remove_file_or_folder(file):
    if os.path.isfile(file):
        os.remove(file)
    elif (os.path.exists(file)):
        shutil.rmtree(file)
    else:
        return -1


def execute_history(op_history):
    history_for_file = dict()
    for operation, filepath, others in op_history:
        if operation != 'mod':
            if filepath in history_for_file:
                history_for_file[filepath] = (operation, others)
            else:
                history_for_file.setdefault(filepath, (operation, others))
        elif operation != 'remarks':  # operation is mod rename
            tmp = history_for_file.get(filepath, None)
            if tmp is not None:  # there has been some changes to the original file
                history_for_file.pop(others, None)
                remove_file_or_folder(filepath)
                history_for_file.setdefault(others, tmp)
            else:  # there is no change in the file content, just move
                history_for_file.setdefault(others, ('mod', filepath))  # SPECIAL: filepath is the source file
    if DEBUG: print(history_for_file)
    for file in history_for_file:
        operation, others = history_for_file[file]
        if operation == 'del':
            remove_file_or_folder(file)
        elif operation == 'mod':
            shutil.move(others, file)
        elif operation == 'upd' or operation == 'new':
            ri = requests.get(currentserver + ":" + port + "/getfile", data={'filename': file})
            file = open(file, 'w')
            data = ri.json()['data']
            file.write(data)
            file.close()
