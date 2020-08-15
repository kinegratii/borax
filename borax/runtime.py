# coding=utf8


import time
from collections import defaultdict
from contextlib import contextmanager


class RuntimeMeasurer:
    def __init__(self):
        self._data = defaultdict(list)
        self._start_time_dict = {}

    def start(self, tag, *tags):
        tags = (tag,) + tags
        st = time.time()
        for _tag in tags:
            self._start_time_dict[_tag] = st

    def end(self, tag, *tags):
        tags = (tag,) + tags
        et = time.time()
        for _tag in tags:
            if _tag in self._start_time_dict:
                self._data[_tag].append(et - self._start_time_dict[_tag])

    @contextmanager
    def measure(self, tag, *tags):
        try:
            self.start(tag, *tags)
            yield
        finally:
            self.end(tag, *tags)

    def get_measure_data(self):
        data = []
        for tag, values in self._data.items():
            data.append({
                'tag': tag,
                'total': len(values),
                'avg': sum(values) / len(values)
            })
        return data
