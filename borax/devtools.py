import time
from collections import defaultdict, namedtuple
from contextlib import contextmanager

from typing import Dict

TagMeasureResult = namedtuple('TagMeasureResult', 'name total count avg')


class RuntimeMeasurer:
    """A time measurer for a program."""

    def __init__(self):
        self._data = defaultdict(list)
        self._start_time_dict = {}

    def start(self, *tags: str) -> 'RuntimeMeasurer':
        st = time.time()
        for _tag in tags:
            self._start_time_dict[_tag] = st
        return self

    def end(self, *tags: str) -> 'RuntimeMeasurer':
        et = time.time()
        for _tag in tags:
            if _tag in self._start_time_dict:
                self._data[_tag].append(et - self._start_time_dict[_tag])
        return self

    @contextmanager
    def measure(self, *tags: str):
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

    def print_(self):
        """Print statistics data for all tags."""
        data = self.get_measure_result()
        print("{:>8} {:>10} {:>10} {:>10}".format('name', 'total', 'count', 'avg'))
        for v in data.values():
            name, total, count, avg = v
            print(f"{name:>8} {total:>.8f} {count:>10} {avg:>.8f}")
