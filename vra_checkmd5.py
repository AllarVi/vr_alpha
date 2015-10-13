# coding=utf-8
import json
import vra_http_request_helper
from md5 import vra_md5

__author__ = 'allar'


def send_answermd5(masterData):
    sendip = masterData['ip']
    sendport = masterData['port']
    request_id = masterData['id']
    md5_hash = masterData['md5']
    ranges = masterData['ranges']

    my_ip = vra_http_request_helper.get_my_ip()
    my_port = vra_http_request_helper.get_my_port()

    print("/checkmd5: templates to try: " + str(ranges))
    result = 0
    result_string = ''
    for range in ranges:
        result_string = vra_md5.md5_crack(str(md5_hash), str(range))
        if result_string:
            result = 1
            print("cracking " + str(md5_hash) + " gave " + result_string)
            break
        else:
            print("failed to crack " + str(md5_hash))
    jdata = json.dumps({"ip":my_ip,
                        "port":my_port,
                        "id":request_id,
                        "md5":md5_hash,
                        "result":result,
                        "resultstring":result_string
                        })
    vra_http_request_helper.send_post_request(sendip, sendport, jdata, "/answermd5")
    print("Sent /answermd5")
    return 0
