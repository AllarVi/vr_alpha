__author__ = 'Mart'

from vra_io import load_hosts
import urllib2
import threading


def resource_handler(sendip, sendport, ttl, id, noask):
    # Check if I am busy and respond accordingly


    # If TTL > 1, send it to known hosts not in noask list
    ttl = int(ttl)
    if (ttl > 1):
        ttl -= 1

        # If sender is not in noask list, add it to noask list
        noask = noask_string_to_list(noask)
        sender = [sendip, sendport]
        if (sender not in noask):
            noask.append(sender)
        # Check noask list vs known hosts list and generate list of new unique hosts to forward request to
        known_hosts_from_file = load_hosts()
        noask = [x for x in known_hosts_from_file if x not in noask]
        # Send request to each unique host
        # Build request
        request_variables = [sendip, sendport, ttl, id, noask]
        # THIS WILL LEAVE THREADS OPEN: threading.Thread(target=urllib2.urlopen, args=("http://127.0.0.1:5000/test",)).start()




    return "Loaded list " + str(load_hosts()) + str(" Noask list:") + str(noask)
    #return "TO-DO: Return valid response and send requests to all other computers/programs not in noask list."


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
