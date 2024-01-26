"""
显示月历
工具
"""
import tkinter as tk
import webbrowser
from datetime import date, datetime, timedelta
from tkinter import ttk
from tkinter.messagebox import showinfo
from typing import Optional

from borax import __version__ as borax_version
from borax.calendars.festivals2 import FestivalLibrary, WrappedDate
from borax.calendars.lunardate import TextUtils, TERMS_CN, TERM_PINYIN
from borax.calendars.ui import CalendarFrame, FestivalTableFrame
from borax.calendars.utils import ThreeNineUtils
from borax.capp.festival_creator import FestivalCreatePanel

library = FestivalLibrary.load_builtin().sort_by_countdown()

PROJECT_URLS = {
    'home': 'https://github.com/kinegratii/borax'
}

style: ttk.Style = None


class WDateVar(tk.StringVar):
    """A tkinter variable for WrappedDate object.
    Use set_date/get_date instead of set/get function.
    """

    def __init__(self, master=None, value=None, name=None, date_fmt='%Y-%m-%d'):
        super().__init__(master, value, name)
        self._date_object = None
        self._date_fmt = date_fmt

    def set_date(self, d: WrappedDate):
        self._date_object = d
        self.set(d.solar.strftime(self._date_fmt))

    def get_date(self) -> Optional[WrappedDate]:
        raw = self.get()
        if raw:
            solar = datetime.strptime(raw, self._date_fmt)
            return WrappedDate(solar.date())
        else:
            return None


class WCalendarToolDlg(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        notebook = ttk.Notebook(self)
        notebook.pack(side='left', expand=True, fill=tk.BOTH, padx=5, pady=5)

        self._current_selected_index = 0
        self._data_stores = {
            'd1': WDateVar(),
            'd2': WDateVar(),
            'd3': WDateVar(),
        }

        self._entry_hints = {
            'd1': '第一个日期',
            'd2': '第二个日期',
            'd3': '起始日期'
        }

        self._tool_form_frame = ttk.Frame(notebook)
        self._tool_form_frame.pack(side='left', expand=True, fill=tk.BOTH)

        ttk.Label(self._tool_form_frame, text='第一个日期').grid(row=0, column=0, columnspan=2)
        self.day1_entry = ttk.Entry(self._tool_form_frame, textvariable=self._data_stores['d1'])
        self.day1_entry.bind('<FocusIn>', lambda event: self.entry_picker_linked(event, 'd1'))
        self.day1_entry.grid(row=0, column=2, columnspan=2)
        ttk.Label(self._tool_form_frame, text='第二个日期').grid(row=1, column=0, columnspan=2)
        self.day2_entry = ttk.Entry(self._tool_form_frame, textvariable=self._data_stores['d2'])
        self.day2_entry.bind('<FocusIn>', lambda event: self.entry_picker_linked(event, 'd2'))
        self.day2_entry.grid(row=1, column=2, columnspan=2)

        ttk.Button(self._tool_form_frame, text='计算', command=self.run_date_delta).grid(
            row=2, column=0, columnspan=4, pady=8)
        self.result1_label = ttk.Label(self._tool_form_frame, text='')
        self.result1_label.grid(row=3, column=0, columnspan=4)
        notebook.add(self._tool_form_frame, text='日期间隔', padding=4)

        deduction_frame = ttk.Frame(notebook)
        notebook.add(deduction_frame, text='日期推导', padding=4)
        ttk.Label(deduction_frame, text='起始日期').grid(row=0, column=0, columnspan=2)
        self.day3_entry = ttk.Entry(deduction_frame, textvariable=self._data_stores['d3'])
        self.day3_entry.bind('<FocusIn>', lambda event: self.entry_picker_linked(event, 'd3'))
        self.day3_entry.grid(row=0, column=2, columnspan=2)
        self.day_delta_s = tk.IntVar()
        for i, item in enumerate([('向前', -1), ('向后', 1)]):
            t, val = item
            tk.Radiobutton(deduction_frame, text=t, value=val, variable=self.day_delta_s).grid(row=1, column=i * 2 + 1,
                                                                                               columnspan=2)
        ttk.Label(deduction_frame, text='间隔天数').grid(row=2, column=0, columnspan=2)
        self.delta_days = tk.IntVar()
        delta_days_com = ttk.Combobox(deduction_frame, width=6, values=[30, 60, 90, 100, 200, 300, 1000],
                                      textvariable=self.delta_days)
        delta_days_com.grid(row=2, column=2, columnspan=2, sticky=tk.E + tk.W + tk.N + tk.S)
        ttk.Button(deduction_frame, text='计算', command=self.run_date_deduction).grid(
            row=3, column=0, columnspan=4, pady=8)
        self.result2_label = ttk.Label(deduction_frame, text='')
        self.result2_label.grid(row=4, column=0, columnspan=4)
        # init
        self.day_delta_s.set(1)

        # Date Pick Panel
        right_frame = ttk.Frame(self)
        right_frame.pack(side='left')

        self.picker_hint_label = ttk.Label(right_frame, text='请选择第一个日期')
        self.picker_hint_label.pack(side='top', fill=tk.X)
        date_picker = CalendarFrame(right_frame, festival_source=library)
        date_picker.bind_date_selected(self.on_date_picked)
        date_picker.pack(side='top', expand=True, fill=tk.X)

    def entry_picker_linked(self, event, entry_label: str):
        self._current_selected_index = entry_label
        self.picker_hint_label.config(text=f'请选择{self._entry_hints[entry_label]}')

    def on_date_picked(self, wd: WrappedDate):
        if self._current_selected_index in self._data_stores:
            self._data_stores[self._current_selected_index].set_date(wd)

    def run_date_delta(self):
        d1, d2 = self._data_stores['d1'].get_date(), self._data_stores['d2'].get_date()
        if d1 and d2:
            ndays = (d2.solar - d1.solar).days
            self.result1_label.config(text=f'相差 {ndays} 天')
        else:
            self.result1_label.config(text='未选择日期，无法计算')

    def run_date_deduction(self):
        d3 = self._data_stores['d3'].get_date()
        if d3:
            result2 = d3 + timedelta(self.day_delta_s.get() * self.delta_days.get())
            self.result2_label.config(text=str(result2))
        else:
            self.result2_label.config(text='未选择日期，无法计算')


class DateDetailFrame(ttk.LabelFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, text='*****', labelanchor='n', **kwargs)

        self.label_widgets = {}

        # 4 = 121 22
        # -XX-
        self.label_widgets['solar_day'] = ttk.Label(self, text='5', font=('Helvatical bold', 40))
        self.label_widgets['solar_day'].grid(row=0, column=0, rowspan=2, columnspan=4)
        self.label_widgets['solar_ym'] = ttk.Label(self, text='2022年5月')
        self.label_widgets['solar_ym'].grid(row=2, column=0, columnspan=4)

        self.label_widgets['solar_lunar'] = ttk.Label(self, text='四月初三')
        self.label_widgets['solar_lunar'].grid(row=0, column=5, columnspan=2)
        self.label_widgets['solar_week'] = ttk.Label(self, text='星期三')
        self.label_widgets['solar_week'].grid(row=0, column=7, columnspan=2)
        self.label_widgets['solar_gz'] = ttk.Label(self, text='星期三')
        self.label_widgets['solar_gz'].grid(row=1, column=5, columnspan=4)
        self.label_widgets['festival'] = ttk.Label(self, text='')
        self.label_widgets['festival'].grid(row=2, column=5, columnspan=4)

    def set_selected_date(self, wd: WrappedDate = None):
        """Show a date detail in panel.Today is shown if wd is None."""
        if wd is None:
            wd = WrappedDate(date.today())
        sd, ld = wd.solar, wd.lunar

        self.label_widgets['solar_day'].config(text=str(sd.day))
        self.label_widgets['solar_ym'].config(text=sd.strftime('%Y年%m月'))
        self.label_widgets['solar_lunar'].config(text=ld.strftime('%L%M月%D'))
        week_cn = ld.cn_week
        self.label_widgets['solar_week'].config(text=f'星期{week_cn}')
        self.label_widgets['solar_gz'].config(text=ld.gz_str())
        day_labels = library.get_festival_names(sd)
        three_night_label = ThreeNineUtils.get_39label(sd)
        if three_night_label:
            day_labels.append(three_night_label)
        self.label_widgets['festival'].config(text=' '.join(day_labels))


class GanzhiPanel(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        gz_grid_frame = ttk.Frame(self)
        for offset in range(60):
            row, col = offset // 10, offset % 10
            btn_text = '{} {}'.format(TextUtils.offset2gz(offset), offset + 1)
            btn = tk.Button(gz_grid_frame, text=btn_text, width=5, height=1,
                            command=lambda go=offset: self._show_years(go), relief=tk.GROOVE)
            btn.grid(row=row, column=col, ipadx=5, ipady=5)
        gz_grid_frame.pack(side='left')

        self.year_list = ttk.Treeview(self, column=("年份",), show='headings', height=5)
        self.year_list.column("# 1", anchor=tk.CENTER)
        self.year_list.heading("# 1", text="农历年份")
        self.year_list.pack(side='left', expand=True, fill=tk.BOTH)

    def _show_years(self, gz_offset: int):
        for item in self.year_list.get_children():
            self.year_list.delete(item)
        if 0 < gz_offset < 36:
            start_year = 1924 + gz_offset
        else:
            start_year = 1864 + gz_offset
        for year in range(start_year, 2101, 60):
            self.year_list.insert('', 'end', text="1", values=(f"{year}",))


class TermPanel(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        columns = ("序号", "节气", "识别码(拼音首字母)", "太阳地心视黄经（度）")
        self.term_table = ttk.Treeview(self, column=columns, show='headings', height=5)
        self.term_table.pack(side='top', expand=True, fill=tk.BOTH)
        for i, name in enumerate(columns, start=1):
            self.term_table.column(f"# {i}", anchor=tk.CENTER)
            self.term_table.heading(f"# {i}", text=name)

        for tindex, tname in enumerate(TERMS_CN):  # 1-285
            dg = (285 + 15 * tindex) % 360
            self.term_table.insert('', 'end', text="1", values=(tindex, tname, TERM_PINYIN[tindex], dg))


class CApp(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        left_frame = ttk.Frame(self)
        left_frame.pack(side='left', expand=True, fill=tk.Y, padx=10, pady=10)
        self.detail_frame = DateDetailFrame(left_frame)
        self.detail_frame.set_selected_date()
        self.detail_frame.pack(side='top', expand=True, fill=tk.BOTH, pady=5)

        self.cal_panel = CalendarFrame(left_frame, festival_source=library)
        self.cal_panel.pack(side='top', expand=True, fill=tk.BOTH)
        self.cal_panel.bind_date_selected(self.on_show_date_detail)

        ttk.Separator(self, orient=tk.VERTICAL).pack(side='left', fill=tk.Y, expand=True)
        self._table_festival_library = library
        columns = (("name", 120), ("description", 160), ("code", 80), ("next_day", 150), ("countdown", 60))
        self._cs = FestivalTableFrame(self, columns=columns, festival_source=library, countdown_ordered=True)
        self._cs.pack(side='right', expand=True, fill=tk.BOTH, padx=10, pady=10)

        # cs.update_data()
        self._style_var = tk.StringVar()
        self._table_festival_source_var = tk.StringVar(value='basic')
        self.create_top_menu()
        self._tool_dlg = None
        self._gz_dlg = None
        self._festival_create_dlg = None

    def create_top_menu(self):
        top = self.winfo_toplevel()
        menu_bar = tk.Menu(top)
        top['menu'] = menu_bar

        global style

        viewmenu = tk.Menu(menu_bar, tearoff=0)
        for name in style.theme_names():
            viewmenu.add_radiobutton(label=name, variable=self._style_var, command=self._change_theme)
        menu_bar.add_cascade(label='界面主题', menu=viewmenu)
        menu_bar.add_command(label='日期计算', command=self.start_tool_dlg)
        menu_bar.add_command(label='节气干支', command=self.start_gz_dlg)
        menu_bar.add_command(label='创建节日', command=self.start_festival_dlg)
        source_menu = tk.Menu(menu_bar)
        for source in ('basic', 'ext1'):
            source_menu.add_radiobutton(label=source, variable=self._table_festival_source_var,
                                        command=self._change_source)
        menu_bar.add_cascade(label='节日源', menu=source_menu)
        about_menu = tk.Menu(menu_bar)
        about_menu.add_command(label='项目主页', command=lambda: webbrowser.open(PROJECT_URLS['home']))
        about_menu.add_command(label='关于软件', command=self.show_about_info)
        menu_bar.add_cascade(label='关于', menu=about_menu)

    def _change_theme(self):
        global style
        style.theme_use(self._style_var.get())

    def _change_source(self):
        self._cs.change_festival_source(self._table_festival_source_var.get())

    def on_show_date_detail(self, wd: WrappedDate):
        self.detail_frame.set_selected_date(wd)

    def _create_tool_dialog(self):
        self._tool_dlg = tk.Toplevel(self)
        self._tool_dlg.resizable(False, False)
        d = WCalendarToolDlg(self._tool_dlg)
        d.pack(side='top')
        self._tool_dlg.lift()

    def start_tool_dlg(self):
        if self._tool_dlg is None:
            self._create_tool_dialog()
            return
        try:
            self._tool_dlg.lift()
        except tk.TclError:
            self._create_tool_dialog()

    def _create_gz_dialog(self):
        self._gz_dlg = tk.Toplevel(self)
        self._gz_dlg.resizable(False, False)
        notebook = ttk.Notebook(self._gz_dlg)
        tp = TermPanel(notebook)
        notebook.add(tp, text='节气')
        d = GanzhiPanel(notebook)
        notebook.add(d, text='干支')
        notebook.pack(side='top')
        self._gz_dlg.lift()

    def start_gz_dlg(self):
        if self._gz_dlg is None:
            self._create_gz_dialog()
            return
        try:
            self._gz_dlg.lift()
        except tk.TclError:
            self._create_gz_dialog()

    def _create_festival_dialog(self):
        self._festival_create_dlg = tk.Toplevel(self)
        self._festival_create_dlg.title('创建节日')
        self._festival_create_dlg.resizable(False, False)
        festival_create_frame = FestivalCreatePanel(self._festival_create_dlg)
        festival_create_frame.pack(side='top')
        self._festival_create_dlg.lift()

    def start_festival_dlg(self):
        if self._festival_create_dlg is None:
            self._create_festival_dialog()
            return
        try:
            self._festival_create_dlg.lift()
        except tk.TclError:
            self._create_festival_dialog()

    def show_about_info(self):
        showinfo('关于', f' 日历v{borax_version}\n\n Powered by Borax{borax_version}')


def start_calendar_app():
    root = tk.Tk()
    rw, rh = 920, 460
    x, y = int(root.winfo_screenwidth() / 2 - rw / 2), int(root.winfo_screenheight() / 2 - rh / 2)
    root.geometry(f"{rw}x{rh}+{x}+{y}")
    root.resizable(False, False)
    root.title(f'日历 - v{borax_version}')
    global style
    style = ttk.Style(root)
    # style.theme_use('alt')
    app = CApp(root)
    app.pack(expand=True, fill=tk.BOTH)
    root.mainloop()


if __name__ == '__main__':
    start_calendar_app()
