from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    print(request.path)
    print(request.method)
    f = open(request.form['filename'], 'w')
    f.write(request.form['data'])
    f.close()
    # print(request.form[data])
    # print(request.info)
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
