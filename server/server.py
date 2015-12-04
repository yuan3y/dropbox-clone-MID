import os
import shutil
from flask import Flask, jsonify, request
import fileindex
from client_default import *

app = Flask(__name__)

list_of_client = []


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


def clear_redundant_deleted_files():
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
        client_specific_deleted_file_list = deleted_files.keys()  # special case for new client, won't be added to the current deleted file list
    index = fileindex.getIndex(dir=request.form['path'])
    files = index['listfiles']
    folders = index['listfolders']
    for filename in deleted_files:
        if not deleted_files[filename].get(request.remote_addr, True):
            client_specific_deleted_file_list.append(filename)
            deleted_files[filename][request.remote_addr] = True
    clear_redundant_deleted_files()
    json_result = jsonify({'listfiles': files, 'listfolders': folders, 'deleted': client_specific_deleted_file_list})
    return json_result


@app.route('/del', methods=['POST'])
# del files/folders on server
def postDel():
    if (os.path.isfile(request.form['dir'])):
        os.remove(request.form['dir'])
    else:
        shutil.rmtree(request.form['dir'])
    tmp_dict_of_filename_with_client = dict.fromkeys(list_of_client, False)
    tmp_dict_of_filename_with_client[request.remote_addr] = True
    deleted_files.setdefault(request.form['dir'], tmp_dict_of_filename_with_client)
    clear_redundant_deleted_files()


@app.route('/change', methods=['POST'])
# rename files/folders on server
def postRename():
    print(request.form['previousName'])
    print(request.form['newName'])
    if (request.form['modification'] == 'mod'):
        os.rename(request.form['previousName'], request.form['newName'])
    if request.form['newName'] in deleted_files:
        deleted_files.pop(request.form['filename'])
    clear_redundant_deleted_files()


@app.route('/files', methods=['POST'])
# publish changes of files on the server
def postFiles():
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

    if request.form['filename'] in deleted_files:
        deleted_files.pop(request.form['filename'])
    clear_redundant_deleted_files()
    return '', 200


# publish changes of folders on the server
@app.route('/folders', methods=['POST'])
def postDirs():
    # the new folder appeared
    if (request.form['modification'] == 'new'):
        os.makedirs(request.form['dir'])
    if request.form['filename'] in deleted_files:
        deleted_files.pop(request.form['filename'])
    clear_redundant_deleted_files()
    return 200


if __name__ == '__main__':
    serverip = currentserver[6:]
    if not serverip[0].isnumeric():
        serverip = serverip[1:]
    print(serverip)
    app.run(host=serverip)
