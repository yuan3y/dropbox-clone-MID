from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    print(request.path)
    print(request.method)
    print(request.form)
    return 'Hello World!'

if __name__ == '__main__':
    app.run()