import json

__author__ = 'Mart'

import urllib2
import socket
from flask import request
from requests import get




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
    # my_ip_json = json.loads(get('https://api.ipify.org?format=json').text)
    # my_ip = my_ip_json['ip']
    my_ip = socket.gethostbyname(socket.getfqdn())
    #my_host = str(request.host)
    #my_host_separator_index = my_host.index(':')
    #return my_host[:my_host_separator_index]
    # return my_ip
    return get_ip_address('wlan0')

import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def get_my_port():
    my_host = str(request.host)
    my_host_separator_index = my_host.index(':')
    return my_host[my_host_separator_index + 1:]