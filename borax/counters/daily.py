import calendar


class DailyCounter:
    # TODO Use Counter
    def __init__(self, year, month, raw=None):
        self._days = calendar.monthrange(year, month)[1]
        self._year = year
        self._month = month
        if raw:
            try:
                counter = list(map(int, raw.split(',')))
            except (TypeError, ValueError):
                counter = []
            if len(counter) == self._days:
                self._counter = counter
            else:
                raise ValueError('Invalid raw data for %d-%d' % (self._year, self._month))
        else:
            self._counter = [0] * self._days

    def get_day_counter(self, day):
        ii = day - 1
        if ii in range(self._days):
            return self._counter[ii]
        else:
            raise ValueError('Invalid day.Interger 1 - %d expected.' % self._days)

    def increase(self, day, step=1):
        ii = day - 1
        self._counter[ii] += step

    @property
    def days(self):
        return self._days

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    def __iter__(self):
        for val in self._counter:
            yield val

    def __str__(self):
        return ','.join(self._counter)
