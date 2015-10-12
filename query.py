__author__ = 'Mart'

import uuid


class Query:
    last_range_index = 0
    pending_ranges = []

    def __init__(self, md5, wildcard):
        self.query_id = str(uuid.uuid1())
        self.md5 = md5
        self.wildcard = wildcard
