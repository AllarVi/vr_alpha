# coding=utf-8
import json
import socket
from flask import Flask, request, render_template
from vra_md5 import md5_crack
import vra_resource
import getopt, sys
import requests
import uuid
import urllib
import urllib2

app = Flask(__name__)

potentialWorkers = {}

md5 = ''

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['submit'] == 'sendResourceRequests':
            global md5
            md5 = request.form['md5']
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

    workerData = json.loads(str(request.get_data()))

    # Here we will save workers for potential future use, currently not yet implemented
    potentialWorkers[workerData['id']] = workerData

    # Request sender data
    my_host = str(request.host)
    my_host_separator_index = my_host.index(':')
    my_ip = my_host[:my_host_separator_index]
    my_port = my_host[my_host_separator_index + 1:]
    # Worker data
    workerId = str(workerData['id'])
    md5ToCrack = str(md5)

    jdata = json.dumps({"ip":my_ip,
                        "port":my_port,
                        "id":workerId,
                        "md5":md5ToCrack,
                        "ranges":"hereWillBeRanges",
                        "wildcard":"hereWillBeWildcard",
                        "symbolrange":"hereWillBeSymbolRange"
                        })

    # Send md5 to worker
    try:
        workerIp = str(workerData['ip'])
        workerPort = str(workerData['port'])
        urllib2.urlopen("http://" + workerIp + ":" + workerPort + "/checkmd5", jdata, timeout=0.0000001)
    except socket.error:
        print "Socket timeout error as expected."
    except urllib2.URLError as e:
        print "URLError: " + str(e)

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

@app.route('/checkmd5', methods=['POST'])
def checkmd5():
    bruteforceData = json.loads(str(request.get_data()))

    # tocrack="68e1c85222192b83c04c0bae564b493d" # hash of koer
    print('md5 cracker starting...')
    tocrack= str(bruteforceData['md5'])
    res=md5_crack(tocrack,"r???at")
    if res:
        print("cracking "+tocrack+" gave "+res)
    else:
        print("failed to crack "+tocrack)

    return 'success'


@app.route('/answermd5')
def answermd5():
    return 'Hello World!'


def readcmdport(argv):
    try:
        opts, args = getopt.getopt(argv,"p:",["-port"])
    except getopt.GetoptError:
        return int(5001)
    for opt, arg in opts:
        if opt == '-p':
            if arg.isdigit():
                if int(arg) < 65535 and int(arg) > 0:
                    return int(arg)
    return int(5001)


if __name__ == '__main__':
    my_port = readcmdport(sys.argv[1:])
    app.debug = True
    app.run(threaded=True,
            port=my_port)