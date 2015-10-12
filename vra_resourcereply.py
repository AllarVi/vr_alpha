import json
import socket
import urllib2
from flask import request
import vra_http_request_helper
from md5 import vra_range_generator
import time

def send_checkmd5(query, request_id, sendip, sendport, resource):
    if resource is not 0:
        ranges = vra_range_generator.get_range(query.last_range_index, query.wildcard)
        query.last_range_index += 1
        print("Range: " + str(ranges))
        pending_range = {}
        pending_range['id'] = request_id
        pending_range['ranges'] = str(ranges)
        pending_range['timestamp'] = time.time()
        query.pending_ranges[request_id] = pending_range

        my_ip = vra_http_request_helper.get_my_ip()
        my_port = vra_http_request_helper.get_my_port()

        jdata = json.dumps({"ip": my_ip,
                        "port": my_port,
                        "id": request_id,
                        "md5": query.md5,
                        "ranges": ranges,
                        "wildcard": query.wildcard
                        })
        vra_http_request_helper.send_post_request(sendip, sendport, jdata, "/checkmd5")
        print("Query: " + str(query))

    return query