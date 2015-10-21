import urllib2
import socket
from flask import request
import threading

__author__ = 'Mart'


def send_get_request(sendip, sendport, my_params):
    try:
        encodedSendIp = str(sendip)
        encodedSendPort = str(sendport)
        urllib2.urlopen("http://" + encodedSendIp + ":" + encodedSendPort + my_params, timeout=0.0001)
    except socket.error:
        print "Socket timeout error as expected."
    except urllib2.URLError as e:
        print "URLError: " + str(e)


def send_post_request(sendip, sendport, jdata, post_action):
    try:
        encodedSendIp = str(sendip)
        encodedSendPort = str(sendport)
        urllib2.urlopen("http://" + encodedSendIp + ":" + encodedSendPort + post_action, jdata, timeout=0.0001)
    except socket.error:
        print "Socket timeout error as expected."
    except urllib2.URLError as e:
        print "URLError: " + str(e)


def get_my_ip():
    my_host = str(request.host)
    my_host_separator_index = my_host.index(':')
    return my_host[:my_host_separator_index]


def get_my_port():
    my_host = str(request.host)
    my_host_separator_index = my_host.index(':')
    return my_host[my_host_separator_index + 1:]


class ThreadedGet(threading.Thread):
    def __init__(self, sendip, sendport, my_params):
        threading.Thread.__init__(self)
        self.sendip = sendip
        self.sendport = sendport
        self.my_params = my_params

    def run(self):
        try:
            encodedSendIp = str(self.sendip)
            encodedSendPort = str(self.sendport)
            urllib2.urlopen("http://" + encodedSendIp + ":" + encodedSendPort + self.my_params)
        except socket.error:
            print "Socket timeout error."
        except urllib2.URLError as e:
            print "URLError: " + str(e)


class ThreadedPost(threading.Thread):
    def __init__(self, sendip, sendport, jdata, post_action):
        threading.Thread.__init__(self)
        self.sendip = sendip
        self.sendport = sendport
        self.jdata = jdata
        self.post_action = post_action

    def run(self):
        try:
            encodedSendIp = str(self.sendip)
            encodedSendPort = str(self.sendport)
            urllib2.urlopen("http://" + encodedSendIp + ":" + encodedSendPort + self.post_action, self.jdata)
        except socket.error:
            print "Socket timeout error."
        except urllib2.URLError as e:
            print "URLError: " + str(e)