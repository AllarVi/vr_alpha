__author__ = 'Mart'

import vra_io
import vra_http_request_helper
import uuid
import time

def md5_crack_request_handler(query):
    # Check known machines availability
    known_hosts = vra_io.load_hosts()

    for host in known_hosts:
        # generate random ID for client
        uid = str(uuid.uuid1())
        query.waiting_requestreply.append(uid)
        my_ip = vra_http_request_helper.get_my_ip()
        my_port = vra_http_request_helper.get_my_port()

        host_ip = str(host[0])
        host_port = str(host[1])
        my_params = '/resource?sendip=' + my_ip + '&sendport=' + my_port + '&ttl=10&id=' + uid
        vra_http_request_helper.send_get_request(host_ip, host_port, my_params)
    return query

def get_wildcard(request):
    wildcard = request.form['wildcard']
    if not wildcard:
        wildcard = "?"

    return wildcard