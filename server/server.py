import datetime
import os
import os.path
import shutil

from flask import Flask, jsonify, request

import filemeta
from client_default import *

app = Flask(__name__)

list_of_client = []

op_history = dict()


def record_history(client=None, operation='remarks', filename='', other=None):
    # if client not in op_history:
    #     op_history.setdefault(client, [])
    #     return
    global op_history
    if operation == 'remarks':
        op_history[client].append(list((operation, filename, other)))
        print(op_history, "hello")
        return op_history
    for cl in list_of_client:
        if cl not in op_history:
            op_history.setdefault(cl, [])
        if cl != client:
            op_history[cl].append(list((operation, filename, other)))
    # op_history[client].append(operation, filename, other)
    print(op_history, "hello")
    return op_history


def walk_files(list_files, list_folders, directory):
    for name in os.listdir(directory):
        path = os.path.join(directory, name).replace('\\', '/')
        if os.path.isfile(path):
            list_files.append(path)
        if os.path.isdir(path):
            list_folders.append(path)
            walk_files(list_files, list_folders, path)


def get_index(directory="./store"):
    meta_data_dict = dict()
    list_files = []
    list_folders = []
    walk_files(list_files, list_folders, directory)
    for filename in list_files:
        meta_data_dict.setdefault(filename, filemeta.filemeta(filename))
    index = {'listfiles': meta_data_dict, 'listfolders': list_folders}
    return index


@app.route('/getfile', methods=['GET'])
# get 'filename' file on the server
def getFile():
    print(request.form['filename'])
    f = open(request.form['filename'], 'r')
    data = f.read()
    f.close()
    return jsonify({'data': data})


@app.route('/getIndex', methods=['GET'])
# get an index of filemeta and folders
def getIndex():
    if request.remote_addr not in list_of_client:
        list_of_client.append(request.remote_addr)
        print('new connection comes from', request.remote_addr)
    index = get_index(directory=request.form['path'])
    files = index['listfiles']
    folders = index['listfolders']
    json_result = jsonify({'listfiles': files, 'listfolders': folders})
    if DEBUG: print({'listfiles': files, 'listfolders': folders})
    return json_result


@app.route('/getHistory', methods=['GET'])
# get a dictionary corresponding clients to a list of operations since the client's last connection
def getHistory():
    global op_history
    if request.remote_addr not in list_of_client:
        list_of_client.append(request.remote_addr)
        print('new connection comes from', request.remote_addr)
        op_history.setdefault(request.remote_addr, [])  # start an empty list for new client
        record_history(request.remote_addr, operation='remarks', filename=request.remote_addr,
                       other=datetime.datetime.now(datetime.timezone.utc))
    copy = op_history[request.remote_addr].copy()
    json_result = jsonify({'client': request.remote_addr, 'history': copy})
    op_history[request.remote_addr] = []
    record_history(request.remote_addr, operation='remarks', filename=request.remote_addr,
                   other=datetime.datetime.now(datetime.timezone.utc))
    return json_result


@app.route('/del', methods=['POST'])
# del files/folders on server
def postDel():
    record_history(client=request.remote_addr, operation=request.form['modification'], filename=request.form['dir'],
                   other=None)
    if os.path.isfile(request.form['dir']):
        os.remove(request.form['dir'])
    else:
        shutil.rmtree(request.form['dir'])
    return 200


@app.route('/change', methods=['POST'])
# rename files/folders on server
def postRename():
    print(request.form['previousName'])
    print(request.form['newName'])
    if (request.form['modification'] == 'mod'):
        os.rename(request.form['previousName'], request.form['newName'])
    record_history(client=request.remote_addr, operation=request.form['modification'],
                   filename=request.form['previousName'], other=request.form['newName'])


@app.route('/files', methods=['POST'])
# publish changes of files on the server
def postFiles():
    meta = dict()
    meta.setdefault('hash', '')
    if os.path.isfile(request.form['filename']):
        meta = filemeta.filemeta(request.form['filename'])
    # the new file appeared
    if (request.form['modification'] == 'new'):
        try:
            print("at after try-except")
            f = open(request.form['filename'], 'w')
            f.write(request.form['data'])
            f.close()
        except IOError:
            print('There was an error with file' + request.form['filename'])
        print("after try-except")

    # update is up to files
    if (request.form['modification'] == 'upd'):
        try:
            f = open(request.form['filename'], 'w')
            f.write(request.form['data'])
            f.close()
        except IOError:
            print('There was an error with modifying file' + request.form['filename'])
    print("before ending")
    print(meta['hash'])
    print(filemeta.filemeta(request.form['filename']))
    if meta['hash'] != filemeta.filemeta(request.form['filename'])['hash']:
        print(record_history(client=request.remote_addr, operation=request.form['modification'] + 'files',
                             filename=request.form['filename'], other=None))
    return '', 200


# publish changes of folders on the server
@app.route('/folders', methods=['POST'])
def postDirs():
    # the new folder appeared
    if (request.form['modification'] == 'new'):
        os.makedirs(request.form['dir'])
    record_history(client=request.remote_addr, operation=request.form['modification'] + 'folders',
                   filename=request.form['dir'], other=None)
    return 200


if __name__ == '__main__':
    serverip = currentserver[6:]
    if not serverip[0].isnumeric():
        serverip = serverip[1:]
    print(serverip)
    app.run(host=serverip)
