from flask import Flask, jsonify, request, send_from_directory
import os
import shutil

defaultpath = "./store/"
# currentserver = '192.168.43.240'
currentserver = "127.0.0.1"

app = Flask(__name__)

# get 'filename' file on the server
@app.route('/getfile', methods=['GET'])
def getFile():
    print(request.form['filename'])
    f = open(defaultpath + request.form['filename'], 'r')
    data = f.read()
    f.close()
    return jsonify({'data': data})

# get list of all files on the server
@app.route('/getfiles', methods=['GET'])
def getCountFiles():
    filenames_list =  os.listdir(request.form['path'])
    return jsonify({'list': filenames_list})

# del files/folders on server
@app.route('/del', methods=['POST'])

def postDel():
    if (os.path.isfile(request.form['dir'])):
        os.remove(request.form['dir'])
    else:
        shutil.rmtree(request.form['dir'])

# publish changes of files on the server
@app.route('/files', methods=['POST'])

def postFiles():
    # the new file appeared
    if (request.form['modification'] == 'new'):
        try:
            f = open(request.form['filename'], 'w')
            f.write(request.form['data'])
            f.close()
        except IOError:
            print('There was an error with file' + request.form['filename'])

    # some file was modificated
    if (request.form['modification'] == 'mod'):
        try:
            os.remove(request.form['filename'])
            f = open(request.form['newfilename'], 'w')
            f.write(request.form['data'])
            f.close()
        except IOError:
            print('There was an error with  renaming file' + request.form['filename'])

    # update is up to files
    if (request.form['modification'] == 'upd'):
        try:
            f = open(request.form['filename'], 'w')
            f.write(request.form['data'])
            f.close()
        except IOError:
            print('There was an error with modifying file' + request.form['filename'])

    return 'postedFiles'

# publish changes of folders on the server
@app.route('/folders', methods=['POST'])
def postDirs():
    # the new folder appeared
    if (request.form['modification'] == 'new'):
        os.makedirs(request.form['dir'])

    # some file/folder was modificated
    if (request.form['modification'] == 'mod'):
        print('how to do it?')

    return 'PostedDirs'

if __name__ == '__main__':
    app.run(host = currentserver)
    # app.run()

