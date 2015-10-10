# coding=utf-8
import json
import socket
import urllib2

__author__ = 'allar'

from flask import request

def send_answermd5(masterData, res):
    my_host = str(request.host)
    my_host_separator_index = my_host.index(':')
    my_ip = my_host[:my_host_separator_index]
    my_port = my_host[my_host_separator_index + 1:]

    requestId = masterData['id']
    md5 = masterData['md5']
    result = 'mis sai (leidsin stringi: 0, ei leidnud stringi: 1, ei jõudnud rehkendada: 2)'
    resultstring = res

    jdata = json.dumps({"ip":my_ip,
                        "port":my_port,
                        "id":requestId,
                        "md5":md5,
                        "result":result,
                        "resultstring":resultstring
                        })

    try:
        encodedSendIp = str(masterData['ip'])
        encodedSendPort = str(masterData['port'])
        urllib2.urlopen("http://" + encodedSendIp + ":" + encodedSendPort + "/answermd5", jdata, timeout=0.0000001)
    except socket.error:
        print "Socket timeout error as expected."
    except urllib2.URLError as e:
        print "URLError: " + str(e)

    pass
