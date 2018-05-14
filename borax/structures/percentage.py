# coding=utf8


class Percentage:
    """
    Percentage(completed=0, total=100, places=2,)
    """

    def __init__(self, *, total=100, completed=0, places=2, display_fmt='{completed} / {total}'):
        self.total = total
        self.completed = completed
        self._display_fmt = display_fmt
        self._places = places
        # string.format will fails here
        self._percent_fmt = '{0:. f}%'.replace(' ', str(self._places))

    def increase(self, value=1):
        self.completed += value

    def decrease(self, value=1):
        self.completed -= value

    @property
    def percent(self):
        if self.total == 0:
            return 0
        else:
            return round(self.completed / self.total, self._places + 2)

    @property
    def percent_display(self):
        return self._percent_fmt.format(self.percent * 100)

    @property
    def display(self):
        return self._display_fmt.format(completed=self.completed, total=self.total)

    def as_dict(self, prefix=''):
        return {
            prefix + 'total': self.total,
            prefix + 'completed': self.completed,
            prefix + 'percent': self.percent,
            prefix + 'percent_display': self.percent_display,
            prefix + 'display': self.display
        }
