# coding=utf8


import time
from collections import defaultdict, namedtuple
from contextlib import contextmanager

from typing import List, Dict

TagMeasureResult = namedtuple('TagMeasureResult', 'name total count avg')


class RuntimeMeasurer:
    def __init__(self):
        self._data = defaultdict(list)
        self._start_time_dict = {}

    def start(self, *tags: List[str]) -> 'RuntimeMeasurer':
        st = time.time()
        for _tag in tags:
            self._start_time_dict[_tag] = st
        return self

    def end(self, *tags: List[str]) -> 'RuntimeMeasurer':
        et = time.time()
        for _tag in tags:
            if _tag in self._start_time_dict:
                self._data[_tag].append(et - self._start_time_dict[_tag])
        return self

    @contextmanager
    def measure(self, *tags: List[str]):
        try:
            self.start(*tags)
            yield
        finally:
            self.end(*tags)

    def get_measure_result(self) -> Dict[str, TagMeasureResult]:
        result = {}
        for tag, values in self._data.items():
            tv = sum(values)
            cv = len(values)
            result[tag] = TagMeasureResult(tag, tv, cv, tv / cv)
        return result
