"""A module including common calendar widgets.
"""
import calendar
import tkinter as tk
from datetime import date
from tkinter import ttk
from typing import Optional, Union, Tuple, Callable, Dict, Sequence, Any

from borax.calendars.festivals2 import FestivalLibrary, WrappedDate, Festival

__all__ = ['CalendarFrame', 'FestivalTableFrame']


def solar_month(year: int, month: int, dm: int = 1) -> Tuple[int, int]:
    """Return target year/month by delta month."""
    cy, cm = divmod((year * 12 + month - 1 + dm), 12)
    return cy, cm + 1


class CalendarFrame(ttk.Frame):
    """A solar/lunar calendar built by Borax.Calendar."""

    def __init__(self, master=None, firstweekday: int = 0, year: int = 0, month: int = 0,
                 festival_source: Union[str, FestivalLibrary] = 'empty', **kw):
        super().__init__(master, **kw)
        self._firstweekday = firstweekday  # 0 = Monday, 6 = Sunday
        self._week_cns = ['一', '二', '三', '四', '五', '六', '日']
        if year == 0 or month == 0:
            today = date.today()
            year, month = today.year, today.month
        self._v_year = tk.IntVar(value=year)
        self._v_month = tk.IntVar(value=month)
        if isinstance(festival_source, str):
            self._library = FestivalLibrary.load_builtin(festival_source)
        else:
            self._library = festival_source
        self._v_day_matrix = [[tk.StringVar() for _ in range(7)] for _ in range(6)]
        self._d_selected_date = None  # type: Optional[WrappedDate]
        self._callbacks = {}  # type: Dict[str,Callable]
        self._day_cell_indexes = -1, -1  # The cell indexes of first and last day in this month.

        self._cal_obj = calendar.Calendar(firstweekday=self._firstweekday)
        self._init_widgets()
        self._update_calendar_cell_values()

    @property
    def year_and_month(self) -> Tuple[int, int]:
        return self._v_year.get(), self._v_month.get()

    def _init_widgets(self):
        bw, bh = 3, 1
        tool_row_no, head_row_no, week_row_no, day_row_no = range(4)

        today_btn = tk.Button(self, text='今日', relief=tk.GROOVE, command=lambda: self._nav_current_month())
        today_btn.grid(row=0, column=5, sticky='wens', columnspan=2, pady=4)
        pre_btn = tk.Button(self, text='\u25C4', width=bw, height=bh, command=lambda: self.page_to(-1),
                            relief=tk.GROOVE)
        pre_btn.grid(row=head_row_no, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        next_btn = tk.Button(self, text='\u25BA', width=bw, height=bh, command=lambda: self.page_to(1),
                             relief=tk.GROOVE)
        next_btn.grid(row=head_row_no, column=6, sticky=tk.E + tk.W + tk.N + tk.S)

        year_com = ttk.Combobox(self, width=bw * 2, values=list(range(2010, 2030)), textvariable=self._v_year)
        year_com.grid(row=head_row_no, column=1, columnspan=2, sticky=tk.E + tk.W + tk.N + tk.S)
        year_com.bind('<<ComboboxSelected>>', self._update_calendar_cell_values)
        tk.Label(self, text='年', width=bw, ).grid(row=head_row_no, column=3, sticky=tk.E + tk.W + tk.N + tk.S)

        month_com = ttk.Combobox(self, width=bw - 1, values=tuple(range(1, 13)), textvariable=self._v_month)
        month_com.grid(row=head_row_no, column=4, sticky=tk.E + tk.W + tk.N + tk.S)
        month_com.bind('<<ComboboxSelected>>', self._update_calendar_cell_values)
        tk.Label(self, text='月', width=bw).grid(row=head_row_no, column=5, sticky=tk.E + tk.W + tk.N + tk.S)

        for ti, week in enumerate(self._cal_obj.iterweekdays()):
            btn = tk.Label(self, text=self._week_cns[week], width=bw, height=bh)
            btn.grid(row=week_row_no, column=ti, sticky=tk.E + tk.W + tk.N + tk.S)

        for row in range(6):
            for col in range(7):
                btn = tk.Button(self, textvariable=self._v_day_matrix[row][col], width=bw, height=bh,
                                command=lambda pr=row, pc=col: self._on_day_cell_clicked(pr, pc), relief=tk.GROOVE)
                btn.grid(row=row + day_row_no, column=col, ipadx=5, ipady=5)

    def _update_calendar_cell_values(self, event=None):
        year = self._v_year.get()
        month = self._v_month.get()
        cell_index = 0
        _mi, _ma, _left_zero = -1, -1, 0
        for day, text, wd in self._library.iter_month_daytuples(year, month):
            if day == 0:
                day_text = ''
                _left_zero += int(_mi == -1)
            else:
                day_text = '{}\n{}'.format(day, text)
                if day == 1:
                    _mi = cell_index
                _ma += 1
            row, col = cell_index // 7, cell_index % 7
            self._v_day_matrix[row][col].set(day_text)
            cell_index += 1
        _ma += _mi
        self._day_cell_indexes = _mi, _ma
        # Fill the rest cells with empty values.
        for r in range(cell_index // 7, 6):
            for col in range(7):
                self._v_day_matrix[r][col].set('')

    def _nav_current_month(self):
        today = date.today()
        vy, vm = today.year, today.month
        self.page_to(vy, vm)
        self._dispatch('DateSelected', WrappedDate(date.today()))

    def page_to(self, *args: int, trigger: bool = True):
        ny, nm = 0, 0
        cy, cm = self._v_year.get(), self._v_month.get()
        if len(args) == 0:
            today = date.today()
            ny, nm = today.year, today.month
        if len(args) == 1:  # month_offset
            month_offset = args[0]
            ny, nm = solar_month(cy, cm, month_offset)
        elif len(args) == 2:  # year,month
            ny, nm = args
        elif len(args) == 3:  # year, month, month_offset
            ny, nm = solar_month(*args)
        if ny != 0 and (cy, cm) != (ny, ny):
            self._v_year.set(ny)
            self._v_month.set(nm)
            self._update_calendar_cell_values()
            if trigger:
                self._dispatch('PageChanged', ny, nm)

    def _on_day_cell_clicked(self, row, col):
        cell_index = row * 7 + col
        if self._day_cell_indexes[0] <= cell_index <= self._day_cell_indexes[1]:
            day = cell_index - self._day_cell_indexes[0] + 1
            wd = WrappedDate(date(year=self._v_year.get(), month=self._v_month.get(), day=day))
            self._d_selected_date = wd
            self._dispatch('DateSelected', wd)

    def _dispatch(self, name: str, *args, **kwargs):
        callback = self._callbacks.get(name)
        if callback:
            callback(*args, **kwargs)

    def bind_date_selected(self, callback: Callable[[WrappedDate], Any]):
        """Set a callback when date cell is clicked."""
        self._callbacks['DateSelected'] = callback

    def bind_page_changed(self, callback: Callable[[int, int], Any]):
        """Set a callback when page is changed."""
        self._callbacks['PageChanged'] = callback


class FestivalItemAdapter:
    """A helper class for display list data."""
    FIELDS = {'name': '名称', 'description': '描述', 'code': '编码', 'next_day': '下一个日期', 'countdown': '倒计天数'}

    def __init__(self, columns: Sequence):
        self.fields = []
        self.displays = []
        self.widths = []

        for cfg in columns:
            if isinstance(cfg, (list, tuple)):
                _f, _w = cfg
            else:
                _f, _w = cfg, 200
            self.fields.append(_f)
            self.displays.append(FestivalItemAdapter.FIELDS.get(_f))
            self.widths.append(_w)

    def object2values(self, festival: Festival, wd: WrappedDate = None, ndays: int = 0):
        obj_dic = {'code': festival.encode(), 'name': festival.name, 'description': festival.description,
                   'catalog': festival.catalog}
        if wd is None:
            ndays, wd = festival.countdown()
        obj_dic.update({'next_day': wd.simple_str(), 'countdown': str(ndays)})
        return [obj_dic.get(_f) for _f in self.fields]


class FestivalTableFrame(ttk.Frame):
    """A table frame displaying festivals with CURD feature."""

    def __init__(self, master=None, columns: Sequence = None, festival_source: Union[str, FestivalLibrary] = 'empty',
                 **kwargs):
        super().__init__(master=master, **kwargs)
        self._adapter = FestivalItemAdapter(columns)
        if isinstance(festival_source, FestivalLibrary):
            self._library = festival_source
        else:
            self._library = FestivalLibrary.load_builtin(festival_source)
        self._tree = ttk.Treeview(self, column=self._adapter.displays, show='headings')
        self._tree.pack(side='left', fill='both')
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=self._tree.yview)
        verscrlbar.pack(side='right', fill='y', expand=True)
        self._tree.configure(yscrollcommand=verscrlbar.set)
        for i, name in enumerate(self._adapter.displays, start=1):
            self._tree.column(f"# {i}", anchor=tk.CENTER, width=self._adapter.widths[i - 1])
            self._tree.heading(f"# {i}", text=name)

        self.notify_data_changed()

    @property
    def tree_view(self):
        return self._tree

    @property
    def festival_library(self) -> FestivalLibrary:
        return self._library

    @property
    def row_count(self):
        return len(self._tree.get_children())

    def notify_data_changed(self):
        item_iids = self._tree.get_children()
        if len(item_iids):
            self._tree.delete(*item_iids)
        for ndays, wd, festival in self._library.list_days_in_countdown(countdown_ordered=False):
            values = self._adapter.object2values(festival, wd, ndays)
            self._tree.insert('', 'end', text="1", values=values)

    # Data CRUD API.

    def add_festival(self, festival: Festival):
        values = self._adapter.object2values(festival)
        self._tree.insert('', 'end', text="1", values=values)
        self._library.append(festival)

    def add_festivals_from_library(self, new_library: FestivalLibrary):
        for festival in new_library:
            self.add_festival(festival)

    def delete_selected_festivals(self):
        # Get selected item to Delete
        indexes = []
        for selected_item in self._tree.selection():
            indexes.append(self._tree.index(selected_item))
            self._tree.delete(selected_item)
        self._library.delete_by_indexes(indexes)
