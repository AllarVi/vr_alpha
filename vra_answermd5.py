from md5 import vra_range_generator
import time
import json
import vra_http_request_helper

__author__ = 'mart'


def send_new_checkmd5(query, request_id, sendip, sendport, result, result_string):
    # If result already found, do nothing.
    if int(query.result_found) == 1:
        print("Well I ended up here somehow.")
        return query

    # If answer is found, prepare query.
    if int(result) == 0:
        query.result_found = 1
        # To avoid overwriting.
        if query.result is "":
            query.result = result_string
        query.pending_ranges = {}
        query.waiting_requestreply = []
        return query
    elif int(result) == 1:
        new_ranges = vra_range_generator.get_range(query.last_range_index, query.wildcard)
        query.last_range_index += 1
        pending_range = {
            'id':request_id,
            'ranges':str(new_ranges),
            'timestamp':time.time()
        }
        my_ip = vra_http_request_helper.get_my_ip()
        my_port = vra_http_request_helper.get_my_port()
        # Assign new value to old pending_range of the same node
        query.pending_ranges[request_id] = pending_range
        jdata = json.dumps({"ip": my_ip,
                        "port": my_port,
                        "id": request_id,
                        "md5": query.md5,
                        "ranges": new_ranges,
                        "wildcard": query.wildcard
                        })
        vra_http_request_helper.send_post_request(sendip, sendport, jdata, "/checkmd5")
    elif int(result) == 2:
        # TODO: reassign ranges
        pass
    return query
