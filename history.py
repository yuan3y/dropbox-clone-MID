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
        if operation == 'remarks':
            pass
        elif operation != 'mod':
            if filepath in history_for_file:
                history_for_file[filepath] = (operation, others)
                if DEBUG: print(filepath,(operation, others)," <= ",operation,filepath,others)
            else:
                history_for_file.setdefault(filepath, (operation, others))
                if DEBUG: print(filepath,(operation, others)," <= ",operation,filepath,others)
        else:  # operation is mod rename
            tmp = history_for_file.get(filepath, None)
            if tmp is not None:  # there has been some changes to the original file
                history_for_file.pop(others, None)
                remove_file_or_folder(filepath)
                history_for_file.setdefault(others, tmp)
                if DEBUG: print(filepath,(tmp)," <= ",operation,filepath,others)
            else:  # there is no change in the file content, just move
                history_for_file.setdefault(others, ('mod', filepath))  # SPECIAL: filepath is the source file
                if DEBUG: print(filepath,(others, ('mod', filepath))," <= ",operation,filepath,others)
    if DEBUG: print(history_for_file)
    for file in history_for_file:
        operation, others = history_for_file[file]
        if operation == 'del':
            remove_file_or_folder(file)
        elif operation == 'newfolders':
            os.mkdir(file)
        elif operation == 'mod':
            try:
                shutil.move(others, file)
            except:
                ri = requests.get(currentserver + ":" + port + "/getfile", data={'filename': file})
                file = open(file, 'w')
                if ri is not None:
                    data = ri.json()['data']
                    file.write(data)
                file.close()
        elif operation == 'updfiles' or operation == 'newfiles':
            ri = requests.get(currentserver + ":" + port + "/getfile", data={'filename': file})
            file = open(file, 'w')
            if ri is not None:
                try:
                    data = ri.json()['data']
                except:
                    data=''
                file.write(data)
            file.close()
