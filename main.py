# coding=utf-8
import json
import getopt
import sys

from flask import Flask, request, render_template, jsonify
from md5 import vra_range_generator

import vra_checkmd5
from md5.vra_md5 import md5_crack
import vra_resource
import vra_resourcereply
import vra_index

app = Flask(__name__)

potentialWorkers = {}

md5 = ''

recievedAnswers = []

is_busy = False

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['submit'] == 'sendResourceRequests':
            global md5
            md5 = request.form['md5']
            vra_index.md5_crack_request_handler(md5)

            return render_template('form_submit.html')
    if request.method == 'GET':
        return render_template('form_submit.html')

@app.route("/resourcereply", methods=['POST'])
def resourcereply():
    global potentialWorkers

    workerData = json.loads(str(request.get_data()))

    # Here we will save workers for potential future use, currently not yet implemented
    potentialWorkers[workerData['id']] = workerData

    print('/resourcereply: My worker has ' + workerData['resource'] + ' resources')
    if (workerData['resource'] == str(100)):
        range_index = 1
        ranges = vra_range_generator.get_range(range_index, '?')
        vra_resourcereply.send_checkmd5(workerData, md5, ranges)
    else:
        print('/resourcereply: My worker is currently busy')

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

    return vra_resource.resource_handler(sendip, sendport, ttl, id, noask, is_busy)

@app.route('/checkmd5', methods=['POST'])
def checkmd5():
    global is_busy
    is_busy = True

    masterData = json.loads(str(request.get_data()))

    # tocrack="68e1c85222192b83c04c0bae564b493d" # hash of koer
    print('md5 cracker starting...')
    tocrack = str(masterData['md5'])

    ranges = masterData['ranges']
    print("/checkmd5: templates to try: " + str(ranges))

    for range in ranges:
        result = md5_crack(tocrack, str(range))
        if result:
            print("cracking " + tocrack + " gave " + result)
            vra_checkmd5.send_answermd5(masterData, result)
        else:
            print("failed to crack " + tocrack)

    is_busy = False

    return 'success'


@app.route('/answermd5', methods=['GET', 'POST'])
def answermd5():
    print('/answermd5 reached...')
    if request.method == 'POST':
        global recievedAnswers

        answerData = json.loads(str(request.get_data()))
        answer = str(answerData['resultstring'])
        worker_ip_and_port = str(answerData['ip']) + ":" + str(answerData['port'])

        recievedAnswers.append((answer, worker_ip_and_port))
        print ('Answer:' + answer)

    if request.method == 'GET':
        return jsonify(resultstring=recievedAnswers)


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
