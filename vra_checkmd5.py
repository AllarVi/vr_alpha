# coding=utf-8
import json
import socket
import urllib2
import vra_http_request_helper

__author__ = 'allar'

from flask import request

def send_answermd5(masterData, res):
    my_ip = vra_http_request_helper.get_my_ip()
    my_port = vra_http_request_helper.get_my_port()

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

    sendip = masterData['ip']
    sendport = masterData['port']

    vra_http_request_helper.send_post_request(sendip, sendport, jdata)

    try:
        encodedSendIp = str(masterData['ip'])
        encodedSendPort = str(masterData['port'])
        urllib2.urlopen("http://" + encodedSendIp + ":" + encodedSendPort + "/answermd5", jdata, timeout=0.0000001)
    except socket.error:
        print "Socket timeout error as expected."
    except urllib2.URLError as e:
        print "URLError: " + str(e)

    pass
