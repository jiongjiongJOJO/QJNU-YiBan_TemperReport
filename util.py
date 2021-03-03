import datetime

def get_time():
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours=-8)
    n_days = now + delta
    return (n_days.strftime("%Y-%m-%d %H:%M:%S"))

def get_time_no_second():
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours=-8)
    n_days = now + delta
    return (n_days.strftime("%Y-%m-%d %H:%M"))

def get_7_day_ago():
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=-7,hours=-8)
    n_days = now + delta
    return n_days.strftime('%Y-%m-%d')


def get_today():
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours=-8)
    n_days = now + delta
    return n_days.strftime("%Y-%m-%d")


def desc_sort(array, key="FeedbackTime"):
    for i in range(len(array) - 1):
        for j in range(len(array) - 1 - i):
            if array[j][key] < array[j + 1][key]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array