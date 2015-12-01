from flask import Flask, jsonify, request, send_from_directory
import os
import shutil

defaultpath = "./store/"
# currentserver = '192.168.43.240'
currentserver = "127.0.0.1"

def walkFiles(listFiles, listFolders, dir):
  for name in os.listdir(dir):
     path = os.path.join(dir, name)
     if os.path.isfile(path):
        listFiles.append(path)
     if os.path.isdir(path):
        listFolders.append(path)
        walkFiles(listFiles, listFolders, path)

app = Flask(__name__)

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
    walkFiles(listfiles, listfolders, request.form['path'])

    for name in listfiles:
        if name in listfolders:
            listfolders.remove(name)

    for name in os.listdir(request.form['path']):
        listfiles.remove(name)

    return jsonify({'listfiles': listfiles, 'listfolders': listfolders})


@app.route('/del', methods=['POST'])
# del files/folders on server
def postDel():
    if (os.path.isfile(request.form['dir'])):
        os.remove(request.form['dir'])
    else:
        shutil.rmtree(request.form['dir'])


@app.route('/change', methods=['POST'])
# rename files/folders on server
def postRename():
    print(request.form['previousName'])
    print(request.form['newName'])
    if (request.form['modification'] == 'mod'):
        os.rename(request.form['previousName'], request.form['newName'])


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

# publish changes of folders on the server
@app.route('/folders', methods=['POST'])
def postDirs():
    # the new folder appeared
    if (request.form['modification'] == 'new'):
        os.makedirs(request.form['dir'])

if __name__ == '__main__':
    app.run(host = currentserver)
    # app.run()

