import calendar
import datetime
from tkinter import Button, Label, Tk, constants
from styles import all


class CurrentDate:
    def __init__(self, year, month, day) -> None:
        self.year = year
        self.month = month
        self.day = day

    def subtract_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1

    def add_month(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1

class MainPageMixin:
    def set_label(self, year, month):
        args = {
            'month_name': calendar.month_name[month],
            'year': year,
        }
        formatted_label = self.template_month_label.format(**args)
        self.month_label.config(text=formatted_label)

    def set_month_days(self, week_day, month_days, current_date):
        for day_count in range(month_days):
            day_index = day_count + week_day
            self.days[day_index].config(text=day_count + 1, **all)
            if self.calendar_instanse.date_is_now(current_date.year, current_date.month, day_count + 1):
                self.days[day_index].config(bg='#0079d8', borderwidth=2)

    def set_days_before_month(self, week_day, back_month_days):
        for before_month_day in range(week_day):
            day_index = week_day - before_month_day - 1
            self.days[day_index].config(text=back_month_days - before_month_day, fg='#707171', bg='#1b1b1b')

    def set_days_after_month(self, month_days, week_day):
        for after_month_day in range(6 * 7 - month_days - week_day):
            day_index = week_day + month_days + after_month_day
            self.days[day_index].config(text=after_month_day + 1, fg='#707171', bg='#1b1b1b')

    def set_days_out_month(self, week_day, month_days, current_date):
        if current_date.month == 1:
            back_month_days = calendar.monthrange(current_date.year - 1, self.calendar_instanse.month_count)[1]
        else:
            back_month_days = calendar.monthrange(current_date.year, current_date.month - 1)[1]

        self.set_days_before_month(week_day, back_month_days)
        self.set_days_after_month(week_day, month_days)

    def set_month(self, current_date: CurrentDate):
        self.set_label(current_date.year, current_date.month)
        week_day, month_days = calendar.monthrange(current_date.year, current_date.month)
        self.set_month_days(week_day, month_days, current_date)
        self.set_days_out_month(week_day, month_days, current_date)

class GUI(MainPageMixin):

    template_month_label = '{month_name}, {year}'

    def __init__(self, calendar_instanse) -> None:
        self.calendar_instanse = calendar_instanse
        self.root = Tk()
        self.root.resizable(0, 0)
        self.root.config(bg='#1b1b1b')

    def main(self, on_back, on_forward):
        self.days = []
        self.month_label = Label(
            self.root,
            anchor=constants.W,
            font='MSSansSerif 12 bold',
            bg='#1b1b1b',
            fg='#fff',
        )
        self.month_label.grid(row=0, column=0, columnspan=5)

        self.back_button = Button(
            self.root,
            bd=0,
            command=on_back,
            activebackground='#0079d8',
            text='<',
            height=3,
            **all,
        )
        self.back_button.grid(row=0, column=5, sticky=constants.NSEW)
        self.forward_button = Button(
            self.root,
            bd=0,
            command=on_forward,
            activebackground='#0079d8',
            text='>',
            **all,
        )
        self.forward_button.grid(row=0, column=6, sticky=constants.NSEW)

        for week_day_index in range(7):
            day_of_week = Label(self.root, text=calendar.day_abbr[week_day_index], **all)
            day_of_week.grid(row=1, column=week_day_index)

        for week in range(6):
            for day in range(7):
                day_label = Label(
                    self.root, text=0, width=6, height=3, highlightcolor='white', **all,
                )
                day_label.grid(row=2 + week, column=day, sticky=constants.NSEW)
                self.days.append(day_label)

    def run(self):
        self.root.mainloop()

class Calendar:
    month_count = 12

    def __init__(self):
        self.datenow = datetime.datetime.now()
        self.current_date = CurrentDate(
            self.datenow.year,
            self.datenow.month,
            self.datenow.day,
        )

        self.gui = GUI(self)
        self.gui.main(self.back, self.forward)
        self.gui.set_month(self.current_date)

    def date_is_now(self, year, month, day):
        month_is_now = self.datenow.month == month
        year_is_now = self.datenow.year == year
        day_is_now = self.datenow.day == day
        return month_is_now and year_is_now and day_is_now

    def back(self):
        self.current_date.subtract_month()
        self.gui.set_month(self.current_date)

    def forward(self):
        self.current_date.add_month()
        self.gui.set_month(self.current_date)


if __name__ == '__main__':
    calendar_instanse = Calendar()
    calendar_instanse.gui.run()
