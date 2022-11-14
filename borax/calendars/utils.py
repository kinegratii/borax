import calendar
from collections import OrderedDict
from datetime import date, datetime, timedelta
from typing import Union, Dict

from borax.calendars.lunardate import LunarDate, TextUtils, TermUtils

__all__ = ['SCalendars', 'ThreeNineUtils']


class SCalendars:
    @staticmethod
    def get_last_day_of_this_month(year: int, month: int) -> date:
        return date(year, month, calendar.monthrange(year, month)[-1])

    @staticmethod
    def get_fist_day_of_year_week(year: int, week: int) -> date:
        fmt = f'{year}-W{week}-1'
        return datetime.strptime(fmt, "%Y-W%W-%w").date()


class ThreeNineUtils:
    """三伏数九天工具函数
    """

    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        """获取公历year年的三伏数九天对应的公历日期。
        """
        day13 = TermUtils.day_start_from_term(year, '夏至', 3, '庚')
        day23 = day13 + timedelta(days=10)
        day33 = TermUtils.day_start_from_term(year, '立秋', 1, '庚')
        day19 = TermUtils.day_start_from_term(year, '冬至', 0)
        days = OrderedDict({
            '初伏': day13,
            '中伏': day23,
            '末伏': day33,
            '一九': day19
        })
        for i, dc in enumerate(TextUtils.DAYS_CN[1:10], start=1):
            days[f'{dc}九'] = day19 + timedelta(days=(i - 1) * 9)
        return days

    @staticmethod
    def get_39label(date_obj: Union[date, LunarDate]) -> str:
        """返回三伏数九天对应的标签，如果不是，返回空字符串。
        """
        if isinstance(date_obj, LunarDate):
            sd = date_obj.to_solar_date()
        else:
            sd = date_obj
        if sd.month in (4, 5, 6, 10, 11):
            return ''
        year = sd.year - bool(sd.month < 4)
        days = ThreeNineUtils.get_39days(year)
        for vs in list(days.items()):
            label, sd = vs
            range_len = -1
            if label in ['初伏', '末伏']:
                range_len = 10
            elif label == '中伏':
                range_len = (days['末伏'] - days['中伏']).days
            elif '九' in label:
                range_len = 9
            offset = (date_obj - sd).days
            if 0 <= offset <= range_len - 1:
                return f'{label}第{offset + 1}天'
        return ''
