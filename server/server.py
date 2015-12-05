import datetime
import os
import shutil
from flask import Flask, jsonify, request
import fileindex
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
    if operation=='remarks':
        op_history[client].append(list((operation,filename,other)))
        print(op_history, "hello")
        return op_history
    for cl in list_of_client:
        if cl not in op_history:
            op_history.setdefault(cl, [])
        if cl!=client:
            op_history[cl].append(list((operation, filename, other)))
    # op_history[client].append(operation, filename, other)
    print(op_history, "hello")
    return op_history


@app.route('/getfile', methods=['GET'])
# get 'filename' file on the server
def getFile():
    print(request.form['filename'])
    f = open(request.form['filename'], 'r')
    data = f.read()
    f.close()
    return jsonify({'data': data})


@app.route('/getfiles', methods=['GET'])
# get list of all files/dirs on the server
def getCountFiles():
    listfiles = os.listdir(request.form['path'])
    listfolders = os.listdir(request.form['path'])
    fileindex.walkFiles(listfiles, listfolders, request.form['path'])

    for name in listfiles:
        if name in listfolders:
            listfolders.remove(name)

    for name in os.listdir(request.form['path']):
        listfiles.remove(name)

    return jsonify({'listfiles': listfiles, 'listfolders': listfolders})


deleted_files = dict()


def clear_redundant_deleted_files(path=None):
    for filename in deleted_files:
        if all(deleted_files[filename]):
            deleted_files.pop(filename)


@app.route('/getIndex', methods=['GET'])
# get an index of filemeta and folders
def getIndex():
    client_specific_deleted_file_list = []
    if request.remote_addr not in list_of_client:
        list_of_client.append(request.remote_addr)
        print('new connection comes from', request.remote_addr)
        client_specific_deleted_file_list = list(
            deleted_files.keys())  # special case for new client, won't be added to the current deleted file list
    index = fileindex.getIndex(dir=request.form['path'])
    files = index['listfiles']
    folders = index['listfolders']
    for filename in deleted_files:
        if not deleted_files[filename].get(request.remote_addr, True):
            client_specific_deleted_file_list.append(filename)
            deleted_files[filename][request.remote_addr] = True
    clear_redundant_deleted_files(request.path)
    json_result = jsonify({'listfiles': files, 'listfolders': folders, 'deleted': client_specific_deleted_file_list})
    if DEBUG: print({'listfiles': files, 'listfolders': folders, 'deleted': client_specific_deleted_file_list})
    return json_result



@app.route('/getHistory', methods=['GET'])
# get a dictionary corresponding clients to a list of operations since the client's last connection
def getHistory():
    global op_history
    if request.remote_addr not in list_of_client:
        list_of_client.append(request.remote_addr)
        print('new connection comes from', request.remote_addr)
        op_history.setdefault(request.remote_addr, [])  # start an empty list for new client
        record_history(request.remote_addr,operation='remarks',filename=request.remote_addr, other=datetime.datetime.now(datetime.timezone.utc))
    copy = op_history[request.remote_addr].copy()
    json_result = jsonify({'client': request.remote_addr, 'history': copy})
    op_history[request.remote_addr]=[]
    record_history(request.remote_addr,operation='remarks',filename=request.remote_addr, other=datetime.datetime.now(datetime.timezone.utc))
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
    # tmp_dict_of_filename_with_client = dict.fromkeys(list_of_client, False)
    # tmp_dict_of_filename_with_client[request.remote_addr] = True
    # deleted_files.setdefault(request.form['dir'], tmp_dict_of_filename_with_client)
    # clear_redundant_deleted_files(request.path)
    return 200


@app.route('/change', methods=['POST'])
# rename files/folders on server
def postRename():
    print(request.form['previousName'])
    print(request.form['newName'])
    if (request.form['modification'] == 'mod'):
        os.rename(request.form['previousName'], request.form['newName'])
    # if request.form['newName'] in deleted_files:
    #     deleted_files.pop(request.form['filename'])
    # clear_redundant_deleted_files(request.path)
    record_history(client=request.remote_addr, operation=request.form['modification'],
                   filename=request.form['previousName'], other=request.form['newName'])


@app.route('/files', methods=['POST'])
# publish changes of files on the server
def postFiles():
    meta = dict()
    meta.setdefault(hash,'')
    if os.path.isfile(request.form['filename']):
        meta=filemeta.filemeta(request.form['filename'])
    # the new file appeared
    if (request.form['modification'] == 'new'):
        try:
            f = open(request.form['filename'], 'w')
            f.write(request.form['data'])
            f.close()
        except IOError:
            print('There was an error with file' + request.form['filename'])

    # update is up to files
    if (request.form['modification'] == 'upd'):
        try:
            f = open(request.form['filename'], 'w')
            f.write(request.form['data'])
            f.close()
        except IOError:
            print('There was an error with modifying file' + request.form['filename'])

    # if request.form['filename'] in deleted_files:
    #     deleted_files.pop(request.form['filename'])
    # clear_redundant_deleted_files(request.path)
    # print (meta, filemeta.filemeta(request.form['filename']))
    if meta[hash] != filemeta.filemeta(request.form['filename'])[hash]:
        record_history(client=request.remote_addr, operation=request.form['modification'] + 'files', filename=request.form['filename'], other=None)
    return '', 200


# publish changes of folders on the server
@app.route('/folders', methods=['POST'])
def postDirs():
    # the new folder appeared
    if (request.form['modification'] == 'new'):
        os.makedirs(request.form['dir'])
    # if request.form['filename'] in deleted_files:
    #     deleted_files.pop(request.form['filename'])
    # clear_redundant_deleted_files(request.path)
    record_history(client=request.remote_addr, operation=request.form['modification'] + 'folders',
                   filename=request.form['dir'], other=None)
    return 200


if __name__ == '__main__':
    serverip = currentserver[6:]
    if not serverip[0].isnumeric():
        serverip = serverip[1:]
    print(serverip)
    app.run(host=serverip)
