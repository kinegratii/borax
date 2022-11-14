import operator
import tkinter as tk
from tkinter import ttk, filedialog
from typing import Union

from borax.calendars.festivals2 import (
    FestivalLibrary, FestivalSchema, FreqConst, SolarFestival, Festival, WeekFestival, LunarFestival, TermFestival
)
from borax.calendars.lunardate import TextUtils, TERMS_CN
from borax.calendars.ui import FestivalTableFrame

__all__ = ['FestivalCreatePanel']


class ChoicesCombobox(ttk.Combobox):
    def __init__(self, master=None, choices=None, val_variable=None, empty_value: Union[int, str] = -1,
                 value_selected=None, **kw):
        self._val_variable = val_variable
        self._empty_value = empty_value
        choices = choices or ()
        self._values, displays = zip(*choices)
        super().__init__(master=master, values=displays, state='readonly', **kw)
        self.bind('<<ComboboxSelected>>', self._widget2variable)
        if self._val_variable:
            # set trigger for self._val_variable.set(xxx)
            self._val_variable.trace('w', self._variable2widget)
        self._value_selected = value_selected

    def _widget2variable(self, event=None):
        if self._val_variable:
            index = self.current()
            if index == -1:
                val = self._empty_value
            else:
                val = self._values[index]
            self._val_variable.set(val)
            if self._value_selected:
                self._value_selected(val)

    def _variable2widget(self, var, index, mode):
        val = self._val_variable.get()
        try:
            pos = self._values.index(val)
            self.current(pos)
        except ValueError:
            pass


class ValidateError(Exception):
    pass


class VarModel:
    def __init__(self):
        self._vars = {
            'name': tk.StringVar(), 'catalog': tk.StringVar(), 'schema': tk.IntVar(),
            's_freq': tk.IntVar(), 's_month': tk.IntVar(), 's_reverse': tk.IntVar(), 's_day': tk.IntVar(),
            'l_freq': tk.IntVar(), 'l_leap': tk.IntVar(), 'l_month': tk.IntVar(), 'l_reverse': tk.IntVar(),
            'l_day': tk.IntVar(),
            'w_month': tk.IntVar(), 'w_index': tk.IntVar(), 'w_week': tk.IntVar(),
            't_term': tk.IntVar(), 't_delta': tk.IntVar(), 't_index': tk.IntVar(), 't_day_gz': tk.StringVar(),
        }

    @property
    def vars(self):
        return self._vars

    def set(self, **kwargs):
        for k, v in kwargs.items():
            if v is not None:
                self._vars[k].set(v)

    def gets(self, *args: str) -> list:
        """Get multiple values."""
        return [self._vars[k].get() for k in args]

    def validate(self) -> Festival:
        name = self._vars['name'].get()
        if not name:
            raise ValidateError('名称不能为空')
        schema = self._vars['schema'].get()
        func = operator.methodcaller(f'_validate_f{schema}')
        festival: Festival = func(self)
        festival.set_name(name)
        return festival

    def init(self):
        data = {
            's_freq': FreqConst.YEARLY, 's_month': 1, 's_reverse': 1, 's_day': 1,
            'l_freq': FreqConst.YEARLY, 'l_leap': 3, 'l_reverse': 1, 'l_month': 1, 'l_day': 1,
            'w_month': 1, 'w_index': 1, 'w_week': 0,
            't_term': 0, 't_delta': 0, 't_index': 0, 't_day_gz': '甲',
        }
        self.set(**data)

    def _validate_f0(self):
        freq, month, reverse, day = self.gets('s_freq', 's_month', 's_reverse', 's_day')
        festival = SolarFestival(day=reverse * day, freq=freq, month=month)
        return festival

    def _validate_f1(self):
        freq, leap, reverse, month, day = self.gets('l_freq', 'l_leap', 'l_reverse', 'l_month', 'l_day')
        festival = LunarFestival(day=reverse * day, freq=freq, leap=leap, month=month)
        return festival

    def _validate_f2(self):
        month, index, week = self.gets('w_month', 'w_index', 'w_week')
        festival = WeekFestival(month=month, index=index, week=week)
        return festival

    def _validate_f4(self):
        term, delta, index, day_gz = self.gets('t_term', 't_delta', 't_index', 't_day_gz')
        festival = TermFestival(term=term, nth=delta * index, day_gz=day_gz)
        return festival


class MessageLabel(ttk.Label):
    def splash(self, text: str, timeout: int = 1000, foreground='black', **kwargs):
        self.config({'text': text, 'foreground': foreground, **kwargs})
        if timeout != 0:
            self.after(timeout, self._clear)

    def _clear(self):
        self.config({'text': ''})


class FestivalCreatePanel(ttk.Frame):
    """A UI panel with festival-CRUD futures."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        lf = ttk.LabelFrame(self, labelanchor='n', text='节日管理工具')
        lf.pack(side='top', fill='x', padx=10, pady=10, expand=True)
        ttk.Label(lf, text='  本工具支持创建公历型、农历型、星期型、节气型节日，并导出为csv文件。').pack(
            side='top', padx=5, pady=5, fill='both', expand=True)

        self._vm = VarModel()

        n_row, s_row, l_row, w_row, t_row, btn_row, msg_row = 0, 2, 4, 6, 8, 10, 11
        empty_rows = (1, 3, 5, 7, 9)
        ccb_w = 10

        freq_choices = ((FreqConst.YEARLY, '每年'), (FreqConst.MONTHLY, '每月'))
        leap_choices = [(3, '平/闰'), (0, '平'), (1, '闰')]
        month_choices = [(0, '---')] + [(m, str(m)) for m in range(1, 13)]
        day_reverse_choices = [(1, '正向'), (-1, '倒数')]
        week_choices = list(enumerate('一二三四五六日'))
        term_choices = list(enumerate(TERMS_CN))
        index_choices = [(i, f'第{i}个') for i in range(1, 10)]
        index2_choices = [(i, f'第{i}个') for i in range(1, 10)] + [(-i, f'倒数第{i}个') for i in range(1, 10)]
        delta_choices = [(0, '当日'), (-1, '之前'), (1, '之后')]
        gz_day_choices = list(TextUtils.BRANCHES + TextUtils.STEMS)

        frame = ttk.Frame(self)
        frame.pack(side='top', expand=True, fill=tk.BOTH, padx=10, pady=10)
        ttk.Label(frame, text='名称').grid(row=n_row, column=0)
        ttk.Entry(frame, textvariable=self._vm.vars['name']).grid(row=n_row, column=1, columnspan=3, sticky='we')
        ttk.Label(frame, text='分类').grid(row=n_row, column=4)
        ttk.Entry(frame, textvariable=self._vm.vars['catalog']).grid(row=n_row, column=5, columnspan=3, sticky='we')
        # Solar Festival
        ttk.Radiobutton(frame, text='公历型', value=FestivalSchema.SOLAR.value, variable=self._vm.vars['schema']).grid(
            row=s_row, column=0)
        ChoicesCombobox(frame, choices=freq_choices, val_variable=self._vm.vars['s_freq'], width=ccb_w).grid(row=s_row,
                                                                                                             column=1)
        ChoicesCombobox(frame, choices=month_choices, val_variable=self._vm.vars['s_month'], width=ccb_w).grid(
            row=s_row, column=3)
        ttk.Label(frame, text='月').grid(row=s_row, column=4)
        ChoicesCombobox(frame, choices=day_reverse_choices, val_variable=self._vm.vars['s_reverse'], width=ccb_w).grid(
            row=s_row, column=5)
        ttk.Combobox(frame, values=list(range(1, 32)), textvariable=self._vm.vars['s_day'], width=ccb_w).grid(row=s_row,
                                                                                                              column=6)
        ttk.Label(frame, text='日/天').grid(row=s_row, column=7)

        # Lunar Festival
        ttk.Radiobutton(frame, text='农历型', value=FestivalSchema.LUNAR.value, variable=self._vm.vars['schema']).grid(
            row=l_row,
            column=0)
        ChoicesCombobox(frame, choices=freq_choices, val_variable=self._vm.vars['l_freq'], width=ccb_w).grid(row=l_row,
                                                                                                             column=1)
        ChoicesCombobox(frame, choices=leap_choices, val_variable=self._vm.vars['l_leap'], width=ccb_w).grid(row=l_row,
                                                                                                             column=2)
        ChoicesCombobox(frame, choices=month_choices, val_variable=self._vm.vars['l_month'], width=ccb_w).grid(
            row=l_row, column=3)
        ttk.Label(frame, text='月').grid(row=l_row, column=4)
        ChoicesCombobox(frame, choices=day_reverse_choices, val_variable=self._vm.vars['l_reverse'], width=ccb_w).grid(
            row=l_row, column=5)
        ttk.Combobox(frame, values=list(range(1, 31)), textvariable=self._vm.vars['l_day'], width=ccb_w).grid(row=l_row,
                                                                                                              column=6)
        ttk.Label(frame, text='日/天').grid(row=l_row, column=7)
        # Week Festival
        ttk.Radiobutton(frame, text='星期型', value=FestivalSchema.WEEK.value, variable=self._vm.vars['schema']).grid(
            row=w_row, column=0)
        ttk.Label(frame, text='每年').grid(row=w_row, column=1)
        ChoicesCombobox(frame, choices=month_choices, val_variable=self._vm.vars['w_month'], width=ccb_w).grid(
            row=w_row, column=3)
        ttk.Label(frame, text='月').grid(row=w_row, column=4)
        ChoicesCombobox(frame, choices=index2_choices, val_variable=self._vm.vars['w_index'], width=ccb_w).grid(
            row=w_row, column=5, columnspan=1)
        ttk.Label(frame, text='星期').grid(row=w_row, column=6, columnspan=1)
        ChoicesCombobox(frame, choices=week_choices, val_variable=self._vm.vars['w_week'], width=ccb_w).grid(
            row=w_row, column=7, columnspan=1)

        # Term Festival
        ttk.Radiobutton(frame, text='节气型', value=FestivalSchema.TERM.value, variable=self._vm.vars['schema']).grid(
            row=t_row,
            column=0)
        ttk.Label(frame, text='每年').grid(row=t_row, column=1)
        ChoicesCombobox(frame, choices=term_choices, val_variable=self._vm.vars['t_term'], width=ccb_w).grid(
            row=t_row, column=2, columnspan=1)
        ttk.Label(frame, text='节气').grid(row=t_row, column=3)
        ChoicesCombobox(frame, choices=delta_choices, val_variable=self._vm.vars['t_delta'], width=ccb_w).grid(
            row=t_row, column=4, columnspan=1)
        ChoicesCombobox(frame, choices=index_choices, val_variable=self._vm.vars['t_index'], empty_value=0,
                        width=ccb_w).grid(row=t_row, column=5, columnspan=1)
        ttk.Combobox(frame, values=gz_day_choices, textvariable=self._vm.vars['t_day_gz'], state='readonly',
                     width=ccb_w).grid(
            row=t_row, column=6, columnspan=1)
        ttk.Label(frame, text='日').grid(row=t_row, column=7)

        # Toolbar 8 cols
        ttk.Button(frame, text='创建节日', command=self._create).grid(row=btn_row, column=0)
        ttk.Button(frame, text='删除所选', command=self._delete).grid(row=btn_row, column=1)
        ttk.Label(frame, text='节日源：').grid(row=btn_row, column=3)
        source_choices = (('empty', '空白'), ('basic', '基础(basic)'), ('ext1', '扩展1(ext1)'), ('custom', '自定义'))
        self._source_var = tk.StringVar()
        source_cc = ChoicesCombobox(frame, choices=source_choices, val_variable=self._source_var,
                                    value_selected=self._on_source_selected, width=ccb_w)
        source_cc.grid(row=btn_row, column=4)
        source_cc.current(0)
        ttk.Button(frame, text='打开文件', command=self._open_and_add).grid(row=btn_row, column=5)
        ttk.Button(frame, text='导出文件', command=self._export).grid(row=btn_row, column=6)

        self._msg_label = MessageLabel(frame, text='')
        self._msg_label.grid(row=msg_row, column=0, columnspan=10)

        for er in empty_rows:
            ttk.Label(frame).grid(row=er, column=0, columnspan=7)

        # init form values
        self._vm.init()

        self._festival_detail = tk.StringVar()
        frame2 = ttk.Frame(self)
        frame2.pack(side='top', expand=True, fill=tk.BOTH)
        ttk.Label(frame2, textvariable=self._festival_detail).pack(side='top')

        columns = (("name", 100), ("description", 200), ("code", 120), ("next_day", 200), ("countdown", 100))
        self._festival_table = FestivalTableFrame(self, festival_source='empty', columns=columns)
        self._festival_table.pack(side='top', expand=True, fill=tk.BOTH, padx=10, pady=10)

    def _create(self, event=None):
        try:
            festival = self._vm.validate()
            self._festival_table.add_festival(festival)
            self._festival_detail.set(f'{festival.description} {festival.encode()}')
        except ValidateError as e:
            self._msg_label.splash(str(e), foreground='red')

    def _delete(self, event=None):
        self._festival_table.delete_selected_festivals()

    def _export(self, event=None):
        filename = filedialog.asksaveasfilename(parent=self, title='保存到', defaultextension='.csv',
                                                filetypes=(('csv', 'csv'),))
        if filename:
            self._festival_table.festival_library.to_csv(filename)
            self._msg_label.splash('导出成功', foreground='green')

    def _on_source_selected(self, val: str):
        if val == 'custom':
            filename = filedialog.askopenfilename(parent=self, title='选择', defaultextension='.csv',
                                                  filetypes=(('csv', 'csv'),))
            if filename:
                f_library = FestivalLibrary.load_file(filename)
                self._load_new_festival_library(f_library)

    def _open_and_add(self, event=None):
        source_name = self._source_var.get()
        if source_name and source_name != 'custom':
            f_library = FestivalLibrary.load_builtin(source_name)
            self._load_new_festival_library(f_library)

    def _load_new_festival_library(self, f_library: FestivalLibrary):
        self._festival_table.add_festivals_from_library(f_library)
        self._msg_label.splash(f'加载成功,共{self._festival_table.row_count}条', foreground='green')


def main():
    root = tk.Tk()
    root.title('节日创建工具')
    root.resizable(False, False)
    app = FestivalCreatePanel(root)
    app.pack(expand=True, fill=tk.BOTH)
    root.mainloop()


if __name__ == '__main__':
    main()
