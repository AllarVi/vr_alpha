import json
import socket
import urllib2
from flask import request
import vra_http_request_helper

def send_checkmd5(workerData, md5, ranges):

    # Request sender data
    my_host = str(request.host)
    my_host_separator_index = my_host.index(':')
    my_ip = vra_http_request_helper.get_my_ip()
    my_port = vra_http_request_helper.get_my_port()
    # Worker data
    workerId = str(workerData['id'])
    md5ToCrack = str(md5)

    jdata = json.dumps({"ip":my_ip,
                        "port":my_port,
                        "id":workerId,
                        "md5":md5ToCrack,
                        "ranges":ranges,
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