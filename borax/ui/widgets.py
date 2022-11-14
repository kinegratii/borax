import tkinter as tk


class CounterLabel(tk.Label):
    def __init__(self, parent, init_value=0, step=1, **kwargs):
        self._count_value = tk.IntVar()
        self._count_value.set(init_value)
        super().__init__(parent, textvariable=self._count_value, **kwargs)
        self._step = step

    def increase(self, step=None):
        step = step or self._step
        self._count_value.set(self._count_value.get() + step)

    def decrease(self, step=None):
        step = step or self._step
        self._count_value.set(self._count_value.get() - step)

    @property
    def count_value(self):
        return self._count_value.get()

    @count_value.setter
    def count_value(self, value):
        self._count_value.set(value)


class TimerLabel(CounterLabel):
    def __init__(self, parent, interval=1000, **kwargs):
        super().__init__(parent, **kwargs)
        self._interval = interval
        self._state = False
        self._timer_id = None

    def _timer(self):
        if self._state:
            self.increase()
            self._timer_id = self.after(self._interval, self._timer)

    def start_timer(self):
        if not self._state:
            self._state = True
            self._timer()

    def stop_timer(self):
        self._state = False
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None

    def reset(self):
        self.stop_timer()
        self.count_value = 0

    @property
    def state(self):
        return self._state
