import json
import vra_http_request_helper
import vra_io

__author__ = 'Mart'


def resource_handler(sendip, sendport, ttl, id, noask, is_busy):
    # Check if I am busy and respond accordingly
    my_ip = vra_http_request_helper.get_my_ip()
    my_port = vra_http_request_helper.get_my_port()

    resource = str(100)
    if (is_busy):
        resource = str(0)

    jdata = json.dumps({"ip":my_ip, "port":my_port, "id":id, "resource":resource})
    vra_http_request_helper.send_post_request(sendip, sendport, jdata, "/resourcereply")

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
        known_hosts_from_file = vra_io.load_hosts()
        known_hosts_from_web = vra_io.load_hosts_from_web("http://maatriks.eu/web_machines.txt")

        will_ask = [x for x in known_hosts_from_file if x not in noask] # Known hosts not in noask list
        will_ask += [x for x in known_hosts_from_web if x not in noask and x not in will_ask] # Web hosts not in noask list and will_ask list

        # Set up request url parameters
        my_params = "/resource?sendip=" + str(sendip) + "&sendport=" + str(sendport) + "&ttl=" + str(ttl) + "&id=" + str(id)
        for host in noask:
            my_params += "&noask=" + str(host[0]) + "_" + str(host[1])

        # Send requests to each unique host
        print('/resource: hosts in will_ask: ' + str(will_ask))
        for host in will_ask:
            host_ip = str(host[0])
            host_port = str(host[1])
            vra_http_request_helper.send_get_request(host_ip, host_port, my_params)
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