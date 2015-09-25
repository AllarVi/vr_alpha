from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/resource')
def resource():
     print request.args['tala']
     return "Requested: " + request.args['tala']

@app.route('/resourcereply')
def resourcereply():
    return 'Hello World!'

@app.route('/checkmd5')
def checkmd5():
    return 'Hello World!'

@app.route('/answermd5')
def answermd5():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()