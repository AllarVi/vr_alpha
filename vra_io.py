__author__ = 'Mart'

import json
import os

def load_hosts():
    # Look up the directory that the program is located in
    root_dir = os.path.abspath(os.path.dirname(__file__))

    # Open machines.txt and read it
    with open(os.path.join(root_dir, 'machines.txt')) as hosts_file:
         return json.load(hosts_file)