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
import vra_query
import vra_http_request_helper
import vra_answermd5

app = Flask(__name__)

potentialWorkers = {}

md5 = ''

recievedAnswers = []

queries = {}
id_hashmap = {}


is_busy = False

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['submit'] == 'crack_me':
            global queries
            # Get submitted wildcard or '?' if no wildcard was submitted
            wildcard = vra_index.get_wildcard(request)
            # If we already have an answer, do not compute again.
            for query in queries:
                if query.md5 is request.form['md5']:
                    return render_template('form_submit.html')
            query = vra_query.Query(request.form['md5'], wildcard)
            query = vra_index.md5_crack_request_handler(query)
            for request_id in query.waiting_requestreply:
                id_hashmap[request_id] = query.id
            queries[query.id] = query
            #queries = vra_index.md5_crack_request_handler(queries)

            return render_template('form_submit.html')
    if request.method == 'GET':
        return render_template('form_submit.html')


@app.route("/resourcereply", methods=['POST'])
def resourcereply():
    """Gets resourcereply and sends out /checkmd5 to node."""
    # testcurl: curl --request POST http://localhost:5000/resourcereply --data '{"ip":"lokaalhost","port":"666","id":"rammmer","resource":"100"}'
    jdata = json.loads(str(request.get_data()))
    sendip = jdata['ip']
    sendport = jdata['port']
    request_id = jdata['id']
    resource = jdata['resource']
    global queries
    global id_hashmap
    queries[id_hashmap[request_id]] =\
        vra_resourcereply.send_checkmd5(queries[id_hashmap[request_id]], request_id, sendip, sendport, resource)
    print("Query: "+ str(queries[id_hashmap[request_id]]))
    return 0


@app.route('/resource', methods=['GET'])
def resource():
    """Replies to resource request"""
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
    print("reached /checkmd5")
    global is_busy
    is_busy = True

    masterData = json.loads(str(request.get_data()))
    a = vra_checkmd5.send_answermd5(masterData)
    print("Reached the end of /checkmd5")
    is_busy = False
    return 0


@app.route('/answermd5', methods=['GET', 'POST'])
def answermd5():
    print('/answermd5 reached...')
    if request.method == 'POST':
        #global recievedAnswers

        answerData = json.loads(str(request.get_data()))
        sendip = answerData['ip']
        sendport = answerData['port']
        request_id = answerData['id']
        result = answerData['result']
        result_string = answerData['resultstring']
        global queries
        global id_hashmap
        queries[id_hashmap[request_id]] =\
        vra_answermd5.send_new_checkmd5(queries[id_hashmap[request_id]], request_id, sendip, sendport, result, result_string)
        return 0

    if request.method == 'GET':
        global queries
        global recievedAnswers

        # Clear previous answers
        recievedAnswers = []

        for key, elem in queries.items():
            # print("MD5: " + str(queries[key].md5) + " | Result: " + str(queries[key].result))
            recievedAnswers.append((str(queries[key].md5), str(queries[key].result)))

        return jsonify(resultstring=recievedAnswers)


def readcmdport(argv):
    try:
        opts, args = getopt.getopt(argv,"p:h:",["-port", "-host"])
    except getopt.GetoptError:
        return int(5000)
    for opt, arg in opts:
        if opt == '-p':
            if arg.isdigit():
                if int(arg) < 65535 and int(arg) > 0:
                    return int(arg)
    return int(5000)

def readcmdhost(argv):
    try:
        opts, args = getopt.getopt(argv,"p:h:",["-port", "-host"])
    except getopt.GetoptError:
        return '127.0.0.1'
    for opt, arg in opts:
        if opt == '-h':
            return arg
    return '127.0.0.1'


if __name__ == '__main__':
    my_port = readcmdport(sys.argv[1:])
    my_host = readcmdhost(sys.argv[1:])
    app.debug = True
    app.run(threaded=True,
            host=my_host,
            port=my_port)
