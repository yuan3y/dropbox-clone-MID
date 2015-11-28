from flask import Flask
from flask import request
import os

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    print(request.path)
    print(request.method)
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

    # print(request.form[data])
    # print(request.info)
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
