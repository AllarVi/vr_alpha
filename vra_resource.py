__author__ = 'Mart'

from vra_io import load_hosts
import urllib2
import socket
from flask import request
import json


def resource_handler(sendip, sendport, ttl, id, noask):
    # Check if I am busy and respond accordingly
    my_host = str(request.host)
    my_host_separator_index = my_host.index(':')
    my_ip = my_host[:my_host_separator_index]
    my_port = my_host[my_host_separator_index + 1:]
    jdata = json.dumps({"ip":my_ip, "port":my_port, "id":id, "resource":str(100)})
    try:
        urllib2.urlopen("http://" + str(sendip) + ":" + str(sendport) + "/resourcereply", jdata, timeout=0.0000001)
    except socket.error:
        print "Socket timeout error as expected."
    except urllib2.URLError as e:
        print "URLError: " + str(e)

    #Forwarding request
    # Check if TTL is a digit
    if ttl.isdigit():
        ttl = int(ttl)
    else:
        return "TTL not a digit, will not forward this request."
    # If TTL > 1, send it to known hosts not in noask list
    if (ttl > 1):
        ttl -= 1

        # If sender is not in noask list, add it to noask list
        noask = noask_string_to_list(noask)
        sender = [sendip, sendport]
        if (sender not in noask):
            noask.append(sender)

        # Add myself to noask:
        noask.append([my_ip, my_port])

        # Check noask list vs known hosts list and generate list of new unique hosts to forward request to
        known_hosts_from_file = load_hosts()
        will_ask = [x for x in known_hosts_from_file if x not in noask]

        # Set up request url parameters
        my_params = "/resource?sendip=" + str(sendip) + "&sendport=" + str(sendport) + "&ttl=" + str(ttl) + "&id=" + str(id)
        for host in noask:
            my_params += "&noask=" + str(host[0]) + "_" + str(host[1])

        # Send requests to each unique host
        for host in will_ask:
            try:
                urllib2.urlopen("http://" + str(host[0]) + ":" + str(host[1]) + my_params, timeout=0.0000001)
            except socket.error:
                print "Socket timeout error as expected."
            except urllib2.URLError as e:
                print "URLError: " + str(e)
    return str(0)


def noask_string_to_list(noask):
    noask_list = []
    for host_string in noask:
        index_of__ = host_string.index('_')
        if index_of__ >= 0:
            host_ip = host_string[:index_of__]
            host_port = host_string[index_of__ + 1:]
            if host_port.isdigit():
                if int(host_port) >= 0 and int(host_port) <= 65535:
                    noask_list.append([host_ip,host_port])
                else:
                    print("Host port must be an integer between 0 and 65535, instead was: " + str(host_port))
            else:
                print("Host port must be an integer, instead was: " + str(type(host_port)))
    return noask_list
