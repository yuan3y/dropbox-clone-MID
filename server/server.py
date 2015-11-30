from flask import Flask, jsonify, request, send_from_directory
import os

defaultpath = "./store/"
currentserver = '192.168.56.1'

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

# publish changes on the server
@app.route('/', methods=['POST'])
def post():
    # the new file appeared
    if (request.form['modifiation'] == 'new'):
        f = open(request.form['filename'], 'w')
        f.write(request.form['data'])
        f.close()

    # some file was deleted
    if (request.form['modifiation'] == 'del'):
        os.remove(request.form['filename'])

    # some file was modificated
    if (request.form['modifiation'] == 'mod'):
        os.remove(request.form['filename'])
        f = open(request.form['newfilename'], 'w')
        f.write(request.form['data'])
        f.close()

    if (request.form['modifiation'] == 'upd'):
        f = open(request.form['filename'], 'w')
        f.write(request.form['data'])
        f.close()

    return 'Hello World!'

if __name__ == '__main__':
    app.run(host = currentserver)

