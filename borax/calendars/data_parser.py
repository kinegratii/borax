import re
from borax.calendars.lunardate import LunarDate

__all__ = ['strptime']


class LunarDateParser(dict):

    def __init__(self):
        super().__init__({
            'y': r'(?P<y>\d{4})',
            'l': r'(?P<l>[01])',
            'm': r'(?P<m>1[0-2]|[1-9])',
            'A': r'(?P<A>1[0-2]|0[1-9]|[1-9])',
            'd': r'(?P<d>3[0-1]|2[0-9]|1[0-9]|[1-9])',
            'B': r'(?P<B>3[0-1]|2[0-9]|1[0-9]|[1-9])|0[1-9]',
            'Y': r'(?P<Y>[〇一二三四五六七八九十]{4})',
            'L': r'(?P<L>闰?)',
            'M': r'(?P<M>[正一二三四五六七八九十冬腊])',
            'D': r'(?P<D>卅[一二]|廿[一二三四五六七八九]|十[一二三四五六七八九]|初[一二三四五六七八九十]|[二三]十)'
        })

    def pattern(self, fmt):
        fmt = fmt.replace('%C', '%Y年%L%M月%D')
        return self._pattern(fmt)

    def _pattern(self, fmt):
        processed_format = ''
        # The sub() call escapes all characters that might be misconstrued
        # as regex syntax.  Cannot use re.escape since we have to deal with
        # format directives (%m, etc.).
        regex_chars = re.compile(r"([\\.^$*+?\(\){}\[\]|])")
        fmt = regex_chars.sub(r"\\\1", fmt)
        whitespace_replacement = re.compile(r'\s+')
        fmt = whitespace_replacement.sub(r'\\s+', fmt)
        while '%' in fmt:
            directive_index = fmt.index('%') + 1
            processed_format = "%s%s%s" % (processed_format,
                                           fmt[:directive_index - 1],
                                           self[fmt[directive_index]])
            fmt = fmt[directive_index + 1:]
        return "%s%s" % (processed_format, fmt)

    def compile(self, fmt):
        return re.compile(self.pattern(fmt), re.IGNORECASE)

    def parse(self, data_string, date_format):

        format_regex = _cache_dic.get(date_format)
        if not format_regex:
            format_regex = _parser.compile(date_format)
            _cache_dic[date_format] = format_regex

        found = format_regex.match(data_string)
        if not found:
            raise ValueError("time data %r does not match format %r" %
                             (data_string, date_format))
        if len(data_string) != found.end():
            raise ValueError("unconverted data remains: %s" %
                             data_string[found.end():])
        found_dict = found.groupdict()

        year = self.validate_and_return(found_dict, 'yY', 'year')
        leap = self.validate_and_return(found_dict, 'lL', 'leap', 0)  # Optional field
        month = self.validate_and_return(found_dict, 'mMA', 'month')
        day = self.validate_and_return(found_dict, 'dDB', 'day')
        return LunarDate(year, month, day, leap)

    def validate_and_return(self, found_dict, fields, attr_name, default_value=None):
        values = []
        for f in fields:
            if f not in found_dict:
                continue
            raw_value = found_dict[f]
            try:
                value = getattr(self, f'convert_{f}')(raw_value)
            except AttributeError:
                if raw_value == '' and default_value is not None:
                    value = default_value
                else:
                    value = int(raw_value)
            values.append(value)
        if len(values) == 0:
            if default_value is not None:
                return default_value
            raise ValueError(f'Can not find any value match with "{attr_name}".')
        if all(ele == values[0] for ele in values):
            return values[0]
        else:
            raise ValueError(f'Multiple different values found with "{attr_name}".')

    def convert_Y(self, raw_value):
        chars = '〇一二三四五六七八九十'
        return int(''.join([str(chars.index(c)) for c in raw_value]))

    def convert_L(self, raw_value):
        if raw_value == '闰':
            return 1
        else:
            return 0

    def convert_M(self, raw_value):
        return 'X正二三四五六七八九十冬腊'.index(raw_value)

    def convert_D(self, raw_value):
        charts = '十一二三四五六七八九'
        tens = '初十廿卅'
        if raw_value[1] == '十':
            return 'X初二三'.index(raw_value[0]) * 10
        return tens.index(raw_value[0]) * 10 + charts.index(raw_value[1])


_parser = LunarDateParser()
_cache_dic = {}


def strptime(data_string: str, date_format: str) -> LunarDate:
    """Parse a LunarDate object from a whole string."""
    return _parser.parse(data_string, date_format)
