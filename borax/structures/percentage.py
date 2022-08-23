def format_percentage(numerator: int, denominator: int, *, places: int = 2, null_val: str = '-') -> str:
    if denominator == 0:
        return null_val
    percent_fmt = '{0:. %}'.replace(' ', str(places))
    val = round(numerator / denominator, places + 2)
    return percent_fmt.format(val)


class Percentage:
    """A object representing a percentage.

    >>> p = Percentage(34)
    >>> p.completed
    34
    >>> p.percent_display
    '34.00%'
    >>> p.fraction_display
    '34 / 100'
    """

    def __init__(self, *, total: int = 100, completed: int = 0, places: int = 2,
                 display_fmt: str = '{completed} / {total}', null_val: str = '-'):
        self.total = total
        self.completed = completed
        self._display_fmt = display_fmt
        self._places = places
        # string.format will fails here
        self._null_val = null_val

    def increase(self, value: int = 1) -> None:
        self.completed += value

    def decrease(self, value: int = 1) -> None:
        self.completed -= value

    @property
    def percent(self) -> float:
        if self.total == 0:
            return 0
        else:
            return round(self.completed / self.total, self._places + 2)

    @property
    def percent_display(self) -> str:
        """percent format string like '12.34%' """
        return format_percentage(self.completed, self.total, places=self._places, null_val=self._null_val)

    @property
    def fraction_display(self):
        """return a fraction like '34 / 100'"""
        return self._display_fmt.format(completed=self.completed, total=self.total)

    @property
    def display(self) -> str:
        """old alias name for fraction_display'"""
        return self.fraction_display

    def as_dict(self, prefix: str = '') -> dict:
        return {
            prefix + 'total': self.total,
            prefix + 'completed': self.completed,
            prefix + 'percent': self.percent,
            prefix + 'percent_display': self.percent_display,
            prefix + 'display': self.display
        }

    def generate(self, char_total: int = 100) -> str:
        char_completed = int(self.percent * char_total)
        return '|{0}{1}| {2:.2%}'.format(
            '▇' * char_completed,
            '░' * (char_total - char_completed),
            self.percent * 100
        )

    def __str__(self):
        return f'<Percentage:{self.display} {self.percent_display}>'
