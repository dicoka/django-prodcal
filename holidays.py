from calendar import weekday
from .service import check_locale, get_prodcals, cast, cast_single_date
from datetime import timedelta
from calendar import Calendar
from math import ceil
from .settings import *


class ProdCal(Calendar):
    def __init__(self, **kwargs):
        Calendar.__init__(self)
        self.locale = check_locale(kwargs['locale']) if 'locale' in kwargs else DEFAULT_LOCALE
        #self.locale = check_locale(kwargs.get('locale'))
        self.abnomal_dates = get_prodcals(self.locale)
        self.time_per_day = kwargs['tm_day'] if 'tm_day' in kwargs else DEFAULT_TIME_PER_DAY

    def is_work_day(self, *args):
        """Checking if the working day today"""
        the_date = cast_single_date(args)
        return (the_date.weekday() < 5) ^ self.abnomal_dates.is_value(the_date)

    def count_work_days(self, start_date, end_date):
        """Counting the number of working days in the interval"""
        start_date, end_date = cast(start_date, end_date)
        tm_delta = (end_date - start_date).days
        # added for negative days number, to count in past (dicoka)
        if tm_delta < 0:
            start_date = end_date
            tm_delta = -1 * tm_delta
        # ---------------------------------------------------------
        work_days = 0
        for day in range(tm_delta+1):
            curr_date = start_date+timedelta(days=day)
            work_days += 1 if self.is_work_day(curr_date) else 0
        return (work_days)

    def count_holidays(self, start_date, end_date):
        """Counting the number of days off in the interval"""
        tm_delta = 0
        if isinstance(end_date, int):
            tm_delta = end_date
        start_date, end_date = cast(start_date, end_date)

        if not tm_delta:
            tm_delta = (end_date - start_date).days + 1

        holidays = 0
        for day in range(tm_delta):
            curr_date = start_date+timedelta(days=day)
            holidays += 1 if not self.is_work_day(curr_date) else 0
        return holidays

    def get_date_by_work_days(self, start_date, work_days):
        """Calculating the end date by the number of working days"""
        start_date = cast_single_date(start_date)
        days_counter = 0
        work_days_counter = 0
        curr_date = ''
        while work_days_counter != work_days:
            curr_date = start_date + timedelta(days=days_counter)
            if self.is_work_day(curr_date):
                work_days_counter += 1
            days_counter += 1
        return curr_date

    def count_work_time(self, start_date, end_date):
        start_date, end_date = cast(start_date, end_date)
        return self.count_work_days(start_date, end_date)*self.time_per_day

    def get_date_by_work_time(self, start_date, count_time):
        start_date = cast_single_date(start_date)
        days = int(ceil(count_time / float(self.time_per_day)))
        return self.get_date_by_work_days(start_date, days+1)
