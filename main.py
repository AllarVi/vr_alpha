from flask import Flask, request
import vra_resource

app = Flask(__name__)



@app.route('/')
def hello_world():
    # TO-DO:
    # UI for end-user inserting MD5 to crack.
    return 'Hello World!'

@app.route('/resource', methods=['GET', 'POST'])
def resource():
     # Read values from request. Supports both GET and POST, whichever is sent.
     sendip = request.values.get('sendip')
     sendport = request.values.get('sendport')
     ttl = request.values.get('ttl')
     id = request.values.get('id')
     noask = request.values.getlist('noask')
     return vra_resource.resource_handler(sendip, sendport, ttl, id, noask)

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
    app.debug = True
    app.run()