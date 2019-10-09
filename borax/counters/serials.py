# coding=utf8

from itertools import chain

from typing import Iterable, List


def generate_serials(upper: int, num: int = 1, lower: int = 0, serials: Iterable[int] = None) -> List[int]:
    exist_set = set(serials)

    el = len(exist_set)
    if el + num > upper - lower:
        raise ValueError('Can not generate {} serials in [{}, {}].'.format(num, lower, upper))

    if el == 0:
        gen = range(lower, upper)
    else:
        max_value = max(exist_set)
        gen = chain(range(max_value + 1, upper), range(lower, max_value))
    result_list = []
    n = 0
    for i in gen:
        if i not in exist_set:
            result_list.append(i)
            n += 1
            if n == num:
                break
    return result_list


class SerialGenerator:
    def __init__(self, upper: int, lower: int = 0):
        self._lower = lower
        self._upper = upper
        self._data_set = set()

    def generate(self, num: int) -> List[int]:
        result = generate_serials(upper=self._upper, lower=self._lower, num=num, serials=self._data_set)
        self.__add_serials(result)
        return result

    def generate_next_one(self) -> int:
        return self.generate(1)[0]

    def __add_serials(self, serials: Iterable[int]) -> None:
        for serial in serials:
            self._data_set.add(serial)

    def add(self, elements: Iterable[int]) -> None:
        for e in elements:
            self._data_set.add(e)

    def remove(self, elements: Iterable[int]) -> None:
        for e in elements:
            self._data_set.remove(e)


class StringSerialGenerator(SerialGenerator):
    def __init__(self, prefix: str, digits: int = 2, base: int = 10):
        self._prefix = prefix
        self._digits = digits
        num_fmt = {2: 'b', 8: 'o', 10: 'd', 16: 'x'}
        if base not in num_fmt:
            raise ValueError('Invalid base value {}.Choices are: 2, 8, 10, 16'.format(base))
        self._num_fmt = '{{0:0{0}{1}}}'.format(digits, num_fmt[base])
        self._base = base
        super().__init__(lower=0, upper=self._base ** digits - 1)

    def generate(self, num: int) -> List[str]:
        res = super().generate(num)
        return list(map(self._convert, res))

    def generate_next_one(self) -> str:
        return self.generate(1)[0]

    def add(self, elements: List[str]) -> None:
        elements = map(self._parse_serial, elements)
        super().add(elements)

    def remove(self, elements: List[str]) -> None:
        elements = map(self._parse_serial, elements)
        super().remove(elements)

    def _parse_serial(self, element: str) -> int:
        return int(element[-self._digits:], self._base)

    def _convert(self, serial: int) -> str:
        return self._prefix + self._num_fmt.format(serial)
