# coding=utf-8
import json
import socket
import urllib2
import vra_http_request_helper
from md5 import vra_range_generator
import time

__author__ = 'allar'

from flask import request








def send_answermd5(masterData, res):
    print("Reached checkmd5")
    my_ip = vra_http_request_helper.get_my_ip()
    my_port = vra_http_request_helper.get_my_port()

    requestId = masterData['id']
    md5 = masterData['md5']
    #result = 'mis sai (leidsin stringi: 0, ei leidnud stringi: 1, ei jõudnud rehkendada: 2)'
    result = masterData['result']
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

    print('Sending /answermd5 back to master')
    vra_http_request_helper.send_post_request(sendip, sendport, jdata, "/answermd5")
