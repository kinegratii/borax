# coding=utf8
import calendar
from datetime import date, datetime


def get_last_day_of_this_month(year: int, month: int) -> date:
    return date(year, month, calendar.monthrange(year, month)[-1])


def get_fist_day_of_year_week(year: int, week: int) -> date:
    fmt = '{}-W{}-1'.format(year, week)
    return datetime.strptime(fmt, "%Y-W%W-%w").date()
