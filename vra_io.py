import json
import os
import urllib2

__author__ = 'Mart'


def load_hosts():
    # Look up the directory that the program is located in
    root_dir = os.path.abspath(os.path.dirname(__file__))

    # Open machines.txt and read it
    with open(os.path.join(root_dir, 'Resources', 'machines.txt')) as hosts_file:
        return json.load(hosts_file)


def load_hosts_from_web(url):
    response = urllib2.urlopen(url)
    return json.loads(response.read())