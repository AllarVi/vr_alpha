import vra_io
import vra_http_request_helper
import uuid

__author__ = 'Mart'


def md5_crack_request_handler(query):
    # Check known machines availability
    known_hosts_from_file = vra_io.load_hosts()
    known_hosts_from_web = vra_io.load_hosts_from_web("http://maatriks.eu/web_machines.txt")

    will_ask = known_hosts_from_file
    will_ask += [x for x in known_hosts_from_web if x not in will_ask]

    for host in will_ask:
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
