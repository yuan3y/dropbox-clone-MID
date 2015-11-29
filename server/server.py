# import flask
from flask import Flask, request, send_from_directory
import os

defaultpath = "./store/"

app = Flask(__name__)

#
@app.route('/', methods=['GET'])
def getFile():
    filenames_list =  os.listdir(request.form['path'])

    return send_from_directory(request.form['path'], filenames_list[request.form['number']])

@app.route('/getnumfiles', methods=['GET'])
def getCountFiles():
    filenames_list =  os.listdir(request.form['path'])
    print(request.form['path'])
    print(len(filenames_list))
    return str(flask.jsonify(size=filenames_list.size))

#
@app.route('/', methods=['POST'])
def post():
    # print(request.form['newfilename'])
    # print(request.method)
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
    app.run()

