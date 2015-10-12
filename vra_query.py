__author__ = 'Mart'

import uuid


class Query:
    last_range_index = 0
    waiting_requestreply = []
    pending_ranges = {}
    result_found = 0
    result = ""

    def __init__(self, md5, wildcard):
        self.id = str(uuid.uuid1())
        self.md5 = md5
        self.wildcard = wildcard
