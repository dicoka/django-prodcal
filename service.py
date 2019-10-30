from datetime import datetime, timedelta, date
from prodcal.models import ProdCals
from prodcal.prodcals.prod_dict import ProdDict
from .settings import *


def check_locale(locale):
    '''
    if not locale:
        return DEFAULT_LOCALE
    '''
    for l in LOCALE_SUPPORTING:
        if locale.upper() == l[0]:
            return l[0]
    return None
    #raise ValueError("Unnsupported/Unknown locale")


def get_prodcals(locale):
    days_dic = {}
    for entry in ProdCals.objects.filter(locale=locale):
        if entry.year not in days_dic:
            days_dic[entry.year] = {}  ##{1: [], 2: [], 3: [], 4:[], 5: [], 6:[] }
        for d in entry.dates:
            if d.month not in days_dic[d.year]:
                days_dic[d.year][d.month] = []
            days_dic[d.year][d.month].append(d.day)
    return ProdDict(days_dic)
    '''
    pc = import_module('prodcal.prodcals.' + locale.lower())
    return pc.NON_WORK_DAY_DICT, pc.WORK_DAY_DICT
    '''


def get_date_today(day):
    today = datetime.today().date()
    if u'today' == day:
        return today
    elif u'yesterday' == day:
        return today - timedelta(days=1)
    elif u'tomorrow' == day:
        return today + timedelta(days=1)
    raise ValueError('Unknown string format', day)

def calc_days_by_int(start_date, days_int):
    return start_date + timedelta(days=days_int)

def cast(start_date, end_date):
    if isinstance(start_date, (tuple, list)) and isinstance(end_date, (tuple, list)):
        start_date, end_date = date(*start_date), date(*end_date)

    if isinstance(start_date, str):
        start_date = get_date_today(start_date)
    elif isinstance(start_date, (tuple, list)):
        start_date = date(*start_date)

    if isinstance(end_date, (tuple, list)):
        end_date = date(*end_date)
    elif isinstance(end_date, int):
        end_date = calc_days_by_int(start_date, end_date)

    if isinstance(start_date, date) and isinstance(end_date, date):
        pass
    else:
        raise ValueError("Unknown format for parse")

    return start_date, end_date

def cast_single_date(args):
    if isinstance(args, (str, date)): #, unicode
        if isinstance(args, str):
            return get_date_today(args)
        elif isinstance(args, date):
            return args
    elif isinstance(args, (tuple, list)):
        if isinstance(args[0], (str)): #, unicode
            return get_date_today(args[0])
        elif isinstance(args[0], int):
            return date(*args)
        elif isinstance(args[0], date):
            return args[0]


def day_s(days_num):
    last_digit = abs(days_num) % 10
    second_digit = ((days_num - last_digit) / 10) % 10
    if second_digit == 1:
        return 'дней'
    elif last_digit == 1:
        return 'день'
    elif (last_digit > 1) and (last_digit < 5):
        return 'дня'
    else:
        return 'дней'

def day_ss(days_num):
        return ('{0} ' + day_s(days_num)).format(days_num)
