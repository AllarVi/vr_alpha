# coding=utf-8
import json
import socket
from flask import Flask, request, render_template
import vra_resource
import getopt, sys
import requests
import uuid

app = Flask(__name__)

potentialWorkers = []

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['submit'] == 'sendResourceRequests':
            # generate random ID for client
            uid = str(uuid.uuid1())

            try:
                requests.get('http://127.0.0.1:5001/resource?sendip=127.0.0.1&sendport=5000&ttl=10&id=' + uid, timeout=0.001)
            except requests.exceptions.ConnectTimeout as e:
                print "Too slow Mojo!"
            except requests.exceptions.ConnectionError as e:
                print "These aren't the domains we're looking for."
            except requests.exceptions.ReadTimeout as e:
                print "Waited too long between bytes."
            except socket.error:
                print "Socket timeout error as expected."

            return render_template('form_submit.html')

    return render_template('form_submit.html')


@app.route("/resourcereply", methods=['POST'])
def resourcereply():
    global potentialWorkers
    # This is to test the data that we got
    print("Data input to /resourcereply: " + str(request.get_data()))

    # potentialWorkerData = json.loads(request.get_data())

    # string=request.form['yourstring']
    # return render_template('form_action.html', string=string)
    return 'success'


@app.route('/resource', methods=['GET'])
def resource():
    print('/resource AT Client reached...')
    # Read values from request. Supports both GET and POST, whichever is sent.
    sendip = request.values.get('sendip')
    sendport = request.values.get('sendport')
    ttl = request.values.get('ttl')
    id = request.values.get('id')
    noask = request.values.getlist('noask')

    return vra_resource.resource_handler(sendip, sendport, ttl, id, noask)

@app.route('/checkmd5')
def checkmd5():
    return 'Hello World!'


@app.route('/answermd5')
def answermd5():
    return 'Hello World!'


def readcmdport(argv):
    try:
        opts, args = getopt.getopt(argv,"p:",["-port"])
    except getopt.GetoptError:
        return int(5000)
    for opt, arg in opts:
        if opt == '-p':
            if arg.isdigit():
                if int(arg) < 65535 and int(arg) > 0:
                    return int(arg)
    return int(5000)


if __name__ == '__main__':
    my_port = readcmdport(sys.argv[1:])
    app.debug = True
    app.run(threaded=True,
            port=my_port)
