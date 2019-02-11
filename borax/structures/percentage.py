# coding=utf8


class Percentage:
    """
    Percentage(completed=0, total=100, places=2,)
    """

    def __init__(self, *, total: int = 100, completed: int = 0, places: int = 2,
                 display_fmt: str = '{completed} / {total}'):
        self.total = total
        self.completed = completed
        self._display_fmt = display_fmt
        self._places = places
        # string.format will fails here
        self._percent_fmt = '{0:. f}%'.replace(' ', str(self._places))

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
        return self._percent_fmt.format(self.percent * 100)

    @property
    def display(self) -> str:
        return self._display_fmt.format(completed=self.completed, total=self.total)

    def as_dict(self, prefix='') -> dict:
        return {
            prefix + 'total': self.total,
            prefix + 'completed': self.completed,
            prefix + 'percent': self.percent,
            prefix + 'percent_display': self.percent_display,
            prefix + 'display': self.display
        }

    def generate(self, char_total=100) -> str:
        char_completed = int(self.percent * char_total)
        return '|{0}{1}| {2:.2f}%'.format(
            '▇' * char_completed,
            '░' * (char_total - char_completed),
            self.percent * 100
        )
