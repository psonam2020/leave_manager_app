from datetime import datetime

def is_saturday(date):
    return date.weekday() == 5

def is_sunday(date):
    return date.weekday() == 6

def working_days(start, end):
    days = 0
    curr = start
    while curr <= end:
        if curr.weekday() < 5:
            days += 1
        curr = curr.replace(day=curr.day + 1)
    return days
