import json
import vra_http_request_helper
from md5 import vra_range_generator
import time


def send_checkmd5(query, request_id, sendip, sendport, resource):
    if resource is not 0:
        ranges = vra_range_generator.get_range(query.last_range_index, query.wildcard)
        # If generated range is empty, then do not send out the request (out of ranges, this hash is not solved).
        if not ranges:
            # Check if there are any ranges not replied to
            if query.pending_ranges.len > 0:
                max_time = -1
                max_id = ""
                current_time = time.time()

                # Find pending range with largest passed time and send it out.
                for range_id in query.pending_ranges:
                    if current_time - query.pending_ranges[range_id].timestamp > max_time:
                        max_time = current_time - query.pending_ranges[range_id].timestamp
                        max_id = range_id

                # By keeping the original request id, we can accept answers from both the original and new requests.
                request_id = max_id
                ranges = query.pending_ranges[max_id]
                query.last_range_index -= 1 # So it is not affected, see couple of rows below.
            else:
                return query

        query.last_range_index += 1
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
        #vra_http_request_helper.send_post_request(sendip, sendport, jdata, "/check5")
        t = vra_http_request_helper.ThreadedPost(sendip, sendport, jdata, "/checkmd5")
        t.setDaemon(True)
        t.start()
        print("Query: " + str(query))

    return query
