# coding=utf-8
import json
import socket
from flask import Flask, request, render_template
import vra_resource
import getopt, sys
import requests
import uuid
import read_machines

app = Flask(__name__)

potentialWorkers = {}

md5 = ''

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['submit'] == 'sendResourceRequests':
            global md5
            md5 = request.form['md5']
            # read known machines
            machines = read_machines.readMachines("machines.txt")
            for machine in machines:
                # generate random ID for client
                uid = str(uuid.uuid1())

                my_host = str(request.host)
                my_host_separator_index = my_host.index(':')
                my_ip = my_host[:my_host_separator_index]
                my_port = my_host[my_host_separator_index + 1:]

                machine_ip = machine[0].strip('"')
                machine_port = machine[1].strip('"')

                try:
                    requests.get('http://' + machine_ip + ':' + machine_port +'/resource?sendip=' + my_ip + '&sendport=' + my_port + '&ttl=10&id=' + uid, timeout=0.001)
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

    # string=request.form['yourstring']
    return 'success'


@app.route('/resource', methods=['GET'])
def resource():
    print('/resource AT Monika reached...')
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
        return int(5002)
    for opt, arg in opts:
        if opt == '-p':
            if arg.isdigit():
                if int(arg) < 65535 and int(arg) > 0:
                    return int(arg)
    return int(5002)


if __name__ == '__main__':
    my_port = readcmdport(sys.argv[1:])
    app.debug = True
    app.run(threaded=True,
            port=my_port)