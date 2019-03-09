# coding=utf8
"""
Validate with Lunar-Solar-Calendar-Converter as dataset source.
See more detail at https://github.com/isee15/Lunar-Solar-Calendar-Converter

First install requirements

pip install LunarSolarConverter
"""
import time
from datetime import timedelta

from LunarSolarConverter import LunarSolarConverter, Solar

from borax.calendars.lunardate import LunarDate, MIN_SOLAR_DATE, MAX_SOLAR_DATE


def iter_solar_date():
    cur_date = MIN_SOLAR_DATE
    i = 0
    while cur_date <= MAX_SOLAR_DATE or i < 10:
        yield cur_date
        cur_date = cur_date + timedelta(days=1)
        i += 1


converter = LunarSolarConverter()


def validate_lunar():
    t1 = time.time()
    total = 0
    fail = 0
    records = []
    for sd in iter_solar_date():

        ld = LunarDate.from_solar(sd)  # test target
        actual = ld.strftime('%y,%m,%d,%l')

        solar = Solar(sd.year, sd.month, sd.day)
        solar_date_str = '{},{},{}'.format(sd.year, sd.month, sd.day)
        lunar = converter.SolarToLunar(solar)

        expected = '{},{},{},{}'.format(lunar.lunarYear, lunar.lunarMonth, lunar.lunarDay, int(lunar.isleap))

        # solar_date_str = sd.strftime("%Y,%m,%d")
        # rsp = urllib.request.urlopen(url='http://localhost:1337/?src={}'.format(solar_date_str))
        # expected = rsp.read().decode('utf8')

        total += 1
        if actual != expected:
            records.append('{}    {}    {}'.format(solar_date_str, expected, actual))
            fail += 1
    if fail > 0:
        with open('fail_record.txt', 'w') as fp:
            fp.write('\n'.join(records))
    t2 = time.time()
    print('Completed! total:{}, fail:{};time {}s'.format(total, fail, int(t2 - t1)))


if __name__ == '__main__':
    validate_lunar()
