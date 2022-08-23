import re
from itertools import chain

from typing import List, Union, Iterable, Generator, Optional, Callable

# ---------- Custom typing ----------
ElementsType = List[Union[int, str]]


def serial_no_generator(lower: int = 0, upper: int = 10, reused: bool = True, values: Iterable[int] = None) -> \
        Generator[int, None, None]:
    values = values or []
    eset = set(filter(lambda x: lower <= x < upper, values))
    if eset:
        max_val = max(eset)
        if reused:
            gen = chain(range(max_val + 1, upper), range(lower, max_val))
        else:
            gen = range(max_val + 1, upper)
    else:
        gen = range(lower, upper)
    for ele in gen:
        if ele in eset:
            continue
        yield ele


_fmt_re = re.compile(r'\{no(:0(\d+)([bodxX]))?\}')

b2p_dict = {'b': 2, 'o': 8, 'd': 10, 'x': 16, 'X': 16}
p2b_dict = {2: 'b', 8: 'o', 10: 'd', 16: 'x'}


class LabelFormatOpts:
    def __init__(self, fmt_str, base=10, digits=2):

        base_char = p2b_dict[base]
        data = _fmt_re.findall(fmt_str)
        ft = [item[0] for item in data if item[0] != '']
        if ft:
            if all(el == ft[0] for el in ft):
                base_char = ft[0][-1]
                base, digits = b2p_dict.get(base_char), int(ft[0][2:-1])
            else:
                raise ValueError(f'{fmt_str} Define different formatter for no variable.')
        new_field_fmt = '{{no:0{0}{1}}}'.format(digits, base_char)

        self.origin_fmt = fmt_str
        self.normalized_fmt = _fmt_re.sub(new_field_fmt, fmt_str)

        fr_dict = {
            'b': '(?P<no>[01]{{{0}}})'.format(digits),
            'o': '(?P<no>[0-7]{{{0}}})'.format(digits),
            'd': '(?P<no>[0-9]{{{0}}})'.format(digits),
            'x': '(?P<no>[0-9a-f]{{{0}}})'.format(digits),
            'X': '(?P<no>[0-9A-Z]{{{0}}})'.format(digits),
        }

        self.parse_re = re.compile(self.normalized_fmt.replace(new_field_fmt, fr_dict[base_char]))
        self.base = base
        self.digits = digits
        self.base_char = base_char

    def value2label(self, value: int) -> str:
        return self.normalized_fmt.format(no=value)

    def label2value(self, label: str) -> int:
        m = self.parse_re.match(label)
        if m:
            return int(m.group('no'), base=self.base)
        raise ValueError(f'Error Value {label}')


class SerialElement:
    __slots__ = ['value', 'label']

    def __init__(self, value, label):
        self.value = value
        self.label = label


class SerialNoPool:
    def __init__(self, lower: int = None, upper: int = None, base: int = 0, digits: int = 0,
                 label_fmt: Optional[str] = None):

        if label_fmt is None:
            self._opts = None
        else:
            base = base or 10
            digits = digits or 2
            self._opts = LabelFormatOpts(label_fmt, base, digits)
            base = self._opts.base
            digits = self._opts.digits

        if lower is not None and lower < 0:
            raise ValueError(f'lower(={lower}) must be >= 0.')
        if upper is not None and upper <= 0:
            raise ValueError(f'upper(={upper}) must be >= 0.')
        s_set = base and digits
        t_set = lower is not None and upper is not None

        if t_set:
            self._lower, self._upper = lower, upper
            if s_set:
                cl, cu = 0, base ** digits
                if not (lower >= cl and upper <= cu):
                    raise ValueError(f'The lower-upper [{lower},{upper}) is not in [{cl},{cu})')
        else:
            if s_set:
                self._lower, self._upper = 0, base ** digits
            else:
                self._lower, self._upper = 0, 100

        self._values = set()
        self._source = None

    # ---------- Pool Attributes ----------

    @property
    def lower(self):
        return self._lower

    @property
    def upper(self):
        return self._upper

    # ---------- Data API ----------

    def set_elements(self, elements: ElementsType) -> 'SerialNoPool':
        self._values = set()
        self.add_elements(elements)
        return self

    def set_source(self, source: Callable[[], ElementsType]) -> 'SerialNoPool':
        self._source = source
        return self

    def add_elements(self, elements: ElementsType) -> 'SerialNoPool':
        values = self._elements2values(elements)
        for v in values:
            self._values.add(v)
        return self

    def remove_elements(self, elements: ElementsType) -> 'SerialNoPool':
        values = self._elements2values(elements)
        for v in values:
            self._values.remove(v)
        return self

    def _elements2values(self, elements: ElementsType) -> List[int]:
        values = []  # type: List[int]
        for ele in elements:
            if isinstance(ele, int):
                value = ele
            elif isinstance(ele, str):
                value = self._opts.label2value(ele)
            else:
                raise TypeError(f'Invalid element {ele}:unsupported type.')
            if self._lower <= value < self._upper:
                values.append(value)
            else:
                raise ValueError(f'Invalid element {ele}: range error')
        return values

    # ---------- Generate API ----------

    def get_next_generator(self) -> Generator[SerialElement, None, None]:
        """
        This is the low-level method.
        :return:
        """
        if self._source is not None:
            elements = self._source()
            self.set_elements(elements)
        value_gen = serial_no_generator(lower=self._lower, upper=self._upper, values=self._values)
        for value in value_gen:
            if self._opts:
                label = self._opts.value2label(value)
            else:
                label = None
            yield SerialElement(value, label)

    def generate_values(self, num=1) -> List[int]:
        return [se.value for se in self.get_next_generator()][:num]

    def generate_labels(self, num=1) -> List[str]:
        if self._opts is None:
            raise TypeError('The operation generate_labels is not allowed when label_fmt is not set.')
        return [se.label for se in self.get_next_generator()][:num]

    def generate(self, num=1) -> List[str]:
        return self.generate_labels(num)
