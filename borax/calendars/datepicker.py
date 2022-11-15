"""
A module for datepicker.
"""

import tkinter as tk
from typing import Optional

from borax.calendars.festivals2 import WrappedDate
from borax.calendars.ui import CalendarFrame

__all__ = ['DatePickerDialog', 'ask_date']


class DatePickerDialog(tk.Toplevel):
    """A dialog for datepicker."""

    def __init__(self, parent=None, modal=True):
        tk.Toplevel.__init__(self, parent=None)
        self.title('选择日期')
        self._parent = parent
        self._modal = modal
        self._cf = CalendarFrame(self)
        self._cf.bind_date_selected(self._set_date)
        self._cf.pack(side='left')
        self._selected_date = None

    def _set_date(self, wd: WrappedDate):
        self._selected_date = wd
        self.destroy()

    def show(self) -> Optional[WrappedDate]:
        if self._modal:
            self.transient(self._parent)
            self.grab_set()
            self.wait_window()
            return self._selected_date


def ask_date() -> Optional[WrappedDate]:
    """Open a date picker dialog."""
    return DatePickerDialog().show()
